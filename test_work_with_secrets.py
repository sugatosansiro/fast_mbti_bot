import os
from dotenv import load_dotenv

load_dotenv()
# Теперь переменная TOKEN, описанная в файле .env,
# доступна в пространстве переменных окружения 

token = os.getenv('TOKEN')
print(token)  # 5697391909:AAGuHPmOIj7Y6MlFMIsfFUKoom7PpDS3T9c