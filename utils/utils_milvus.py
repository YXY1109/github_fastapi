import time

import torch
from PIL import Image
import cn_clip.clip as clip
from cn_clip.clip import available_models, load_from_name
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

from base import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION
from base.config import CLIP_DOWNLOAD_PATH
from base.dababase import get_session_2
from base.sql_model import Video


def get_chinese_clip():
    """
    加载模型
    :return:
    """
    print("Available models:", available_models())
    # Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50']
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-B-16", device=device,
                                       download_root=CLIP_DOWNLOAD_PATH)
    # model.eval()
    return model, preprocess, device


class ChineseCLIPMilvusTools:

    def __init__(self, coll_name, host=MILVUS_HOST, port=MILVUS_PORT) -> None:
        # ChineseCLIP文字/图片向量化
        self.model, self.preprocess, self.device = get_chinese_clip()
        # Milvus向量数据库+搜索
        self.collection = None
        self.coll_name = coll_name
        self.host = host
        self.port = port
        self.success = False  # milvus collection是否可用
        print(f"ChineseCLIP初始化完成！")

    # 图片向量化
    def extract_image_features(self, img_name):
        # 4通道转3通道，去掉透明A通道
        image_data = Image.open(img_name).convert("RGB")
        infer_data = self.preprocess(image_data).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(infer_data)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy()[0]

    # 文字向量化
    def extract_text_features(self, text):
        text_data = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_data)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()[0]

    # 创建collection对象，类似mysql中的表
    # 图像化web端：http://192.168.170.13:8088/
    def milvus_collection(self, force_delete=False):
        try:
            connections.connect(host=self.host, port=self.port)
            print("连接成功")
            if force_delete:
                print(f'不管是否存在，强制删除集合：{self.coll_name}')
                utility.drop_collection(self.coll_name)
            if utility.has_collection(self.coll_name):
                print(f'已经存在集合：{self.coll_name}，跳过')
                self.success = True
            else:
                print(f'不已经存在集合：{self.coll_name}，开始创建')
                # https://milvus.io/docs/create_collection.md
                auto_id = FieldSchema(name='id', dtype=DataType.INT64, description='id', auto_id=True, is_primary=True)
                v_id = FieldSchema(name='v_id', dtype=DataType.VARCHAR, description='媒资id', max_length=10)
                v_title = FieldSchema(name="v_title", dtype=DataType.VARCHAR, description="标题", max_length=500)
                v_year = FieldSchema(name='v_year', dtype=DataType.VARCHAR, description='年代', max_length=20)
                v_director = FieldSchema(name='v_director', dtype=DataType.VARCHAR, description='导演', max_length=50)
                v_type = FieldSchema(name='v_type', dtype=DataType.VARCHAR, description='媒资类型', max_length=5)
                v_duration = FieldSchema(name='v_duration', dtype=DataType.VARCHAR, description='媒资时长',
                                         max_length=10)
                v_status = FieldSchema(name="v_status", dtype=DataType.VARCHAR, description="0=开启,1=关闭",
                                       max_length=5)
                create_time = FieldSchema(name="create_time", dtype=DataType.VARCHAR, description="创建时间",
                                          max_length=100)
                label_embedding = FieldSchema(name="label_embedding", dtype=DataType.FLOAT_VECTOR,
                                              description="标签", dim=512, is_primary=False)
                description = "IPTV推荐系统-无需求项目"
                fields_list = [auto_id, v_id, v_title, v_year, v_director, v_type, v_duration, v_status, create_time,
                               label_embedding]
                schema = CollectionSchema(
                    fields=fields_list,
                    description=description)
                self.collection = Collection(name=self.coll_name, schema=schema)
                print(f"创建Milvus集合：{self.coll_name}成功")
                # L2通常用于CV，IP通常用于NLP
                # https://milvus.io/docs/build_index.md
                index_params = {
                    'metric_type': 'IP',
                    'index_type': 'IVF_FLAT',
                    'params': {"nlist": 1024}
                }
                self.collection.create_index(field_name='label_embedding', index_params=index_params)
                print("创建Milvus索引成功")
                self.success = True
        except Exception as e:
            self.success = False
            print(f"创建Milvus集合：{self.coll_name}失败: {e}")

    # 加载集合
    def load_collection(self, coll_name=''):
        connections.connect(host=self.host, port=self.port)
        if coll_name:
            collection = Collection(coll_name)
        else:
            collection = Collection(self.coll_name)
        collection.load()
        print(f"加载成功milvus集合：{coll_name}，成功")
        return collection

    # 标签提取特征向量后，往milvus存
    def content_to_milvus(self):
        if self.success:
            print(f"milvus链接成功")
            start = time.time()
            my_session = get_session_2().__next__()
            video_item = my_session.query(Video).filter(Video.status == 0).filter(Video.label != '').all()
            if len(video_item) == 0:
                print("milvus已处理完成")
            else:
                print(f"共{len(video_item)}条数据在处理中。。。")
                id_list = [str(video.id) for video in video_item]
                title_list = [video.title for video in video_item]
                year_list = [str(video.year) for video in video_item]
                director_list = [video.director for video in video_item]
                type_list = [str(video.type) for video in video_item]
                duration_list = [str(video.duration) for video in video_item]
                status_list = [str(video.status) for video in video_item]
                create_time_list = [video.create_time.strftime('%Y-%m-%d %H:%M:%S') for video in video_item]
                # 标签数据向量化
                embedding_label_list = [self.extract_text_features(video.label) for video in video_item]
                print(f"提取特征完成")

                # 批量插入向量库
                collection = Collection(self.coll_name)  # Get an existing collection.
                insert_data = [id_list, title_list, year_list, director_list, type_list, duration_list,
                               status_list, create_time_list, embedding_label_list]
                mr = collection.insert(insert_data)
                print(f"mr:{mr}")
                # 插入的数据存储在内存，需要传输到磁盘
                collection.flush()
                print('向量插入共耗时约 {:.2f} 秒'.format(time.time() - start))
                print("插入完成")
        else:
            print(f"milvus链接失败")

    @staticmethod
    def get_id_distance(milvus_results):
        """
        将milvus结果转为数组
        :param milvus_results:
        :return:
        """
        cid_list = []
        if len(milvus_results) > 0:
            hits = milvus_results[0]
            dis_list = hits.distances
            print(f"对应的距离：{dis_list}")
            for hit in hits:
                cid_list.append(hit.entity.get("v_id"))
        return cid_list

    # limit说明：https://milvus.io/docs/hybridsearch.md
    # limit 最大：16384
    def title_search_title(self, cid, stype, status, text_label):
        """
        联合查询，内容找内容
        :param cid: 视频ID
        :param stype: 视频类型
        :param status: 视频状态
        :param text_label: 标签文本
        :return:
        """
        # 文字特征
        text_features = self.extract_text_features(text_label)
        # 加载向量库
        collection = self.load_collection(self.coll_name)
        # 执行搜索
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
        # 前置条件过滤：指定类型，开启状态
        # expr文档：https://milvus.io/docs/boolean.md
        expr = f' v_type == "{stype}" && v_status == "{status}" && v_id != "{cid}"'
        print(f"milvus常量过滤：{expr}")
        search_param = {
            "data": [text_features],
            "anns_field": "label_embedding",
            "param": search_params,
            "expr": expr,
            "limit": 1000,
            "output_fields": ['v_id']
        }
        search_results = collection.search(**search_param)
        return ChineseCLIPMilvusTools.get_id_distance(search_results)


if __name__ == '__main__':
    """
    图像化web端：http://192.168.170.13:8088/
    
    注意：pymilvus版本要和milvus安装的对应上
    """
    # 初始化
    clip_mil_tool = ChineseCLIPMilvusTools(MILVUS_COLLECTION)
    # 创建集合
    clip_mil_tool.milvus_collection(True)
    # 本地循环写入数据的测试
    clip_mil_tool.content_to_milvus()
