from openai import OpenAI
from zhipuai import ZhipuAI
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import ZhipuAIEmbeddings

from core.config import settings


from langchain_community.chat_models import ChatZhipuAI  # ✅ 正确导入

llm_GLM = ChatZhipuAI(
    temperature=0.5,
    model="glm-4",
    api_key=settings.ZHIPUAI_API_KEY,
)

client_zhipuai = ZhipuAI(api_key=settings.ZHIPUAI_API_KEY)

# Embedding Model
embedding_model = ZhipuAIEmbeddings(
    model="Embedding-3",
    api_key=settings.ZHIPUAI_API_KEY
)

# 图像生成模型
image_generation_model = "cogview-3-flash"

# 图像理解模型
image_understanding_model = "glm-4v-flash"
