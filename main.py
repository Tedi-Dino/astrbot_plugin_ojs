import random
import time
from datetime import datetime, timedelta
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import AstrBotConfig

@register("random_reply_demo", "YourName", "特定用户概率随机回复插件(每日限制版)", "1.3.0")
class RandomReplyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config #
        
        # 记录每分钟频率: { 'group_id': [ts1, ts2] }
        self.msg_history = {} 
        
        # 记录每日限制: { 'group_id_rule_index': timestamp }
        self.daily_history = {}

    def get_logical_date(self, timestamp):
        """
        获取逻辑日期。
        以凌晨 04:00 为界，将时间平移 4 小时，这样 03:59 算前一天，04:01 算新的一天。
        """
        dt = datetime.fromtimestamp(timestamp)
        return (dt - timedelta(hours=4)).date()

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        current_group_id = str(event.message_obj.group_id) #
        
        # --- 1. 白名单预检 ---
        configs = self.config.get("group_configs", [])
        valid_groups = {str(cfg.get("group_id", "")) for cfg in configs}

        if current_group_id not in valid_groups:
            return

        sender_id = str(event.get_sender_id())
        
        # 仅在目标群打印日志
        print(f"\n[DEBUG] 📨 收到目标群消息 Group:{current_group_id} User:{sender_id} Msg:{event.message_str}")

        # --- 2. 遍历规则寻找匹配 ---
        matched_config = None
        matched_index = -1
        
        for index, cfg in enumerate(configs):
            cfg_gid = str(cfg.get("group_id", ""))
            raw_users = cfg.get("target_users", [])
            cfg_users = [str(u) for u in raw_users]
            
            if cfg_gid == current_group_id and sender_id in cfg_users:
                print(f"[DEBUG] ✅ 命中规则 #{index}")
                matched_config = cfg
                matched_index = index
                break 
        
        if not matched_config:
            return

        # --- 3. 每日一次限制检查 (新增核心逻辑) ---
        limit_once = matched_config.get("limit_once_per_day", False)
        if limit_once:
            # 生成该规则的唯一 Key
            rule_key = f"{current_group_id}_rule_{matched_index}"
            last_sent_time = self.daily_history.get(rule_key)
            
            if last_sent_time:
                now_date = self.get_logical_date(time.time())
                last_date = self.get_logical_date(last_sent_time)
                
                if now_date == last_date:
                    print(f"[DEBUG] 🛑 每日限制已触发 (上次发送于 {datetime.fromtimestamp(last_sent_time)}), 本次拦截")
                    return
                else:
                    print(f"[DEBUG] 🌅 新的一天 (04:00刷新)，重置限制")

        # --- 4. 基础参数检查 ---
        reply_list = matched_config.get("reply_list", [])
        if not reply_list:
            return

        # --- 5. 每分钟频率限制 ---
        max_per_min = self.config.get("max_per_minute", 10)
        now = time.time()
        
        if current_group_id not in self.msg_history:
            self.msg_history[current_group_id] = []
        
        self.msg_history[current_group_id] = [
            t for t in self.msg_history[current_group_id] 
            if now - t < 60
        ]
        
        if len(self.msg_history[current_group_id]) >= max_per_min:
            print(f"[DEBUG] ⛔ 触发每分钟频率限制，已拦截")
            return

        # --- 6. 概率与发送 ---
        probability = matched_config.get("reply_probability", 0.0)
        rand_val = random.random()
        print(f"[DEBUG] 🎲 随机点数: {rand_val:.4f} (需 < {probability})")
        
        if rand_val < probability:
            # 记录发送时间 (用于每分钟限制)
            self.msg_history[current_group_id].append(now)
            
            # 记录发送时间 (用于每日限制)
            if limit_once:
                rule_key = f"{current_group_id}_rule_{matched_index}"
                self.daily_history[rule_key] = now
            
            selected_reply = random.choice(reply_list)
            print(f"[DEBUG] 🚀 发送回复: {selected_reply}")
            yield event.plain_result(selected_reply) #
