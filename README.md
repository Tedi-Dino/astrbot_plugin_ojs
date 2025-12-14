# 🍺 AstrBot Plugin: Ojisan Reply (astrbot_plugin_ojs)

> 一个简单好用的 AstrBot 插件，专门用来“蹲点”回复特定群友的发言。
> 不管是复读、玩梗，还是每日打卡，这个插件都能搞定。
> 灵感来自群友，代码来自 AI, 但本人测试可用。感谢 Gemini 3 pro。

## ✨ 能干什么？

* **🎯 精准狙击**：只在指定的群，回复指定的人。
* **📅 每日限次**：支持“每天只回一次”（凌晨 4 点刷新）。适合那种“某某复活了！”或者“早安”类的玩梗，防止群友觉得烦。
* **🛡️ 自动防刷屏**：内置了频率限制，如果触发太频繁会自动暂停，保护你的账号不被风控。
* **🎲 概率触发**：可以设置 1% 到 100% 的概率，制造一点“惊喜”。

## 📦 怎么安装？

1.  在astrbot插件商店安装。
2.  备用方案：把插件下载到你的 AstrBot 插件目录（一般是 `data/plugins`）：
    ```bash
    cd data/plugins
    git clone [https://github.com/Tedi-Dino/astrbot_plugin_ojs.git](https://github.com/Tedi-Dino/astrbot_plugin_ojs.git)
    ```
    然后重载即可

## ⚙️ 配置建议（避坑指南）

这个插件支持给不同的群、不同的人设置完全不一样的规则，配置结构有点深。

**😫 别用 WebUI 点点点：**
因为嵌套层级比较多，在网页上配置会点到手酸。

**😎 推荐做法：**
1.  在 WebUI 里随便填个配置保存一下，生成配置文件。
2.  直接去后台找到 `data/config/astrbot_plugin_ojs_config.json`。
3.  复制下面的模板，改改群号和 QQ 号，直接粘贴进去保存。

### 配置模板参考

```json
{
  "group_configs": [
    {
      "group_id": "12345678",
      "target_users": ["10086"],
      "reply_probability": 1.0,
      "limit_once_per_day": true,
      "_comment": "这是一个每日限制规则，每天凌晨4点刷新，适合周更梗"
    },
    {
      "group_id": "87654321",
      "target_users": ["10010"],
      "reply_probability": 0.01,
      "limit_once_per_day": false,
      "_comment": "这是一个低概率彩蛋，没有每日限制"
    }
  ],
  "max_per_minute": 10
}
