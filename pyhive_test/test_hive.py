from pyhive import hive
import os

def connect_to_hive():
    """连接到Hive服务器"""
    conn = hive.Connection(
        host="localhost",
        port=10000,
    )
    return conn

def create_database(cursor):
    """创建steam_data数据库"""
    cursor.execute("CREATE DATABASE IF NOT EXISTS steam_data")
    print("数据库创建成功或已存在")

def create_user_table(cursor):
    """创建user表"""
    cursor.execute("USE steam_data")
    
    # 创建用户表 - 使用反引号包裹表名，因为user是保留关键字
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS `user` (
        id INT,
        username STRING,
        password STRING
    )
    """
    cursor.execute(create_table_sql)
    print("用户表创建成功或已存在")

def execute_sql_file(cursor, sql_file_path):
    """执行SQL文件"""
    try:
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        
        # 分割SQL语句并执行
        sql_statements = sql_content.split(';')
        for statement in sql_statements:
            statement = statement.strip()
            # 跳过空语句和注释行
            if not statement or statement.startswith('--'):
                continue
                
            print(f"执行SQL语句: {statement}")
            cursor.execute(statement)
            print(f"执行SQL语句成功")
    except FileNotFoundError:
        print(f"找不到SQL文件: {sql_file_path}")
        print(f"当前工作目录: {os.getcwd()}")
        raise

def show_table_data(cursor):
    """显示表中的数据"""
    cursor.execute("SELECT * FROM `user`")
    results = cursor.fetchall()
    print("\n用户表数据:")
    for row in results:
        print(row)

def main():
    """主函数"""
    try:
        # 使用相对路径获取SQL文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # 修正项目根目录计算
        sql_file_path = os.path.join(project_root, "test", "user.sql")
        
        print(f"SQL文件路径: {sql_file_path}")
        
        # 检查文件是否存在
        if not os.path.exists(sql_file_path):
            print(f"错误: SQL文件不存在: {sql_file_path}")
            return
        
        # 连接Hive
        conn = connect_to_hive()
        cursor = conn.cursor()
        
        # 创建数据库和表
        create_database(cursor)
        create_user_table(cursor)
        
        # 执行SQL文件
        execute_sql_file(cursor, sql_file_path)
        
        # 显示数据
        show_table_data(cursor)
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("脚本执行完成！")
        
    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
