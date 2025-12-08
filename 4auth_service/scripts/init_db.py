# scripts/init_db.py
import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

async def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    try:
        # 尝试直接创建表，跳过Alembic
        print("尝试直接创建数据库表...")
        
        import asyncpg
        
        # 使用环境变量中的数据库URL或默认值
        db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/auth_db")
        
        # 解析数据库URL
        # 格式: postgresql://username:password@host:port/database
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "")
        
        # 简单解析
        if "@" in db_url:
            # 有认证信息
            creds_part, host_part = db_url.split("@", 1)
            if ":" in creds_part:
                user, password = creds_part.split(":", 1)
            else:
                user, password = creds_part, ""
            
            if "/" in host_part:
                host_port, database = host_part.split("/", 1)
                if ":" in host_port:
                    host, port = host_port.split(":", 1)
                else:
                    host, port = host_port, "5432"
            else:
                host, port, database = host_part, "5432", "auth_db"
        else:
            # 没有认证信息
            user, password, host, port, database = "postgres", "postgres", "localhost", "5432", "auth_db"
        
        print(f"连接到数据库: {host}:{port}/{database}")
        
        # 连接到PostgreSQL
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=int(port),
            database=database
        )
        
        # 检查表是否已存在
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        existing_tables = {row['table_name'] for row in tables}
        print(f"现有表: {existing_tables}")
        
        # 创建缺失的表
        if 'users' not in existing_tables:
            await conn.execute("""
                CREATE TABLE users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ 创建 users 表")
        
        if 'login_history' not in existing_tables:
            await conn.execute("""
                CREATE TABLE login_history (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    user_agent TEXT,
                    ip_address VARCHAR(45),
                    login_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ 创建 login_history 表")
        
        # 创建索引
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_login_history_user_id ON login_history(user_id)")
        
        await conn.close()
        print("✅ 数据库表创建完成！")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 直接运行异步函数
    success = asyncio.run(init_database())
    sys.exit(0 if success else 1)