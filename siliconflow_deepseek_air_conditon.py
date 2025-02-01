from openai import OpenAI
import os

# -----------------------------------------------------------------------------
# 使用 PowerShell
# 打开 PowerShell（在 “开始” 菜单中搜索 “PowerShell” 并打开）。
# 要为当前用户设置环境变量，可以使用
# $env:SILICONFLOW_API_KEY = "your_api_key"
# 命令。
# 同样，将"your_api_key"替换为实际的 API 密钥。不过，这种方式设置的环境变量只在当前 PowerShell 会话中有效。

# 要永久设置环境变量（对于当前用户），可以使用
# [Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY","your_api_key","User")。
# 如果要设置系统级别的环境变量（需要管理员权限），可以将最后一个参数改为"Machine"，
# 例如
# [Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY","your_api_key","Machine")。
# Set up SILICONFLOW API key
# 记得使用以上方法后，需要关闭vscode后重启vscode，之后点击F5运行python脚本的时候才能生效
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY')

if not SILICONFLOW_API_KEY:
    raise ValueError("SILICONFLOW API key is not set. Please set the SILICONFLOW_API_KEY environment variable.")


client = OpenAI(api_key=SILICONFLOW_API_KEY,base_url="https://api.siliconflow.cn/v1")


system_prompt = '''
你现在需要成为一个我室内的空调控制的决策者；我会将历史温度（每半个小时的室温）告诉你、当前空调的运行状态（开/关）告知你，
你来为我决策是否需要打开空调（空调打开后会自动设定为26度、制热状态，并持续30分钟后自动关闭，通常这样的运行，
能带来2摄氏度左右的室温上升，这样设置的原因在于我希望尽可能的省电），但我又不希望室温长时间的保持在23.5度以下，
因为我个人的舒适温度正好是24度，你听明白了我的意思了么？

好的，我完全理解您的需求。您的核心诉求是：

1. 舒适底线：室温不要长时间低于23.5℃（理想24℃）
2. 节能策略：当需要升温时，空调开30分钟制热26℃（预计升温2℃）
3. 运行逻辑：空调开启后必须满30分钟才能再次判断，避免频繁启停

请提供以下信息：
1. 当前时间
2. 当前空调状态（开/关）
3. 过去4小时内每半小时的温度记录（共8个数据点）
4. 当前实时温度（如可获得）

我将根据温度变化趋势、空调运行时长、以及您设定的阈值进行智能判断，在保证基本舒适的前提下最大限度节省能耗。

示例回答结构：
【空调状态建议】保持关闭
【决策依据】过去3小时温度稳定在24.2-24.5℃之间，当前温度24.3℃，高于舒适阈值无需制热
'''

input = '''
1、当前时间：14:25；
2、当前空调状态：关；
3、历史温度（时间顺序列出）：26、25、25、25、24、23、25、24；
4、当前实时温度：24摄氏度；
'''

stream = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": input,
        }
    ],
    model="deepseek-ai/DeepSeek-V3",
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")