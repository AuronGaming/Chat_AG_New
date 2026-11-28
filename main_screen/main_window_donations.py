"""Управление DonationAlerts Chat_AG"""


class MainWindowDonations:
    """Миксин для работы с DonationAlerts (приём донатов)"""

    def _connect_donation_alerts(self, token: str):
        """Подключиться к DonationAlerts"""
        if not token:
            print("⚠️ DonationAlerts: токен не указан")
            return
        try:
            from platforms.donations.worker import DonationAlertsWorker
            config = {"token": token, "enabled": True}
            self.da_worker = DonationAlertsWorker(config)

            self.da_worker.donation_received.connect(self._on_donation_received)
            self.da_worker.chat_message.connect(self._on_chat_message)
            self.da_worker.platform_connected.connect(
                lambda ch: self.event_bus.platform_connected.emit("donation_alerts", ch)
            )
            self.da_worker.platform_disconnected.connect(
                lambda ch: self.event_bus.platform_disconnected.emit("donation_alerts", ch)
            )
            self.da_worker.platform_error.connect(
                lambda err: self.event_bus.platform_error.emit("donation_alerts", err)
            )

            self.da_worker.start()
            print("✅ DonationAlerts: запуск воркера...")
        except Exception as e:
            print(f"❌ DonationAlerts: ошибка подключения: {e}")

    def _disconnect_donation_alerts(self):
        """Отключиться от DonationAlerts"""
        if hasattr(self, 'da_worker') and self.da_worker:
            self.da_worker.stop()
            self.da_worker = None
            print("🔌 DonationAlerts: отключено")

    def _on_donation_received(self, platform: str, username: str, amount: float,
                              currency: str, message: str):
        """Получен донат"""
        print(f"💰 Донат: {username} — {amount} {currency}")

        donate_text = f"💰 {username} задонатил {amount} {currency}"
        if message:
            donate_text += f": {message}"

        self.chat_log.add_chat_message(platform, "DONATION", donate_text,
                                       "#FFD700", emotes={}, gifs=[])

        # Озвучка доната
        self._init_tts()
        if self.tts and self.tts.enabled and not self.tts.mute_donate:
            self.tts.speak(
                f"{username} задонатил {amount} {currency}. {message}",
                is_donate=True
            )

    def _load_donation_settings(self):
        """Загрузить настройки DonationAlerts и автоподключиться"""
        from core.settings_manager import SettingsManager
        s = SettingsManager()
        connections = s.settings.get("connections", {})
        da_config = connections.get("donation_alerts", {})
        if da_config.get("enabled") and da_config.get("token"):
            print("🔄 DonationAlerts: автоподключение по настройкам...")
            self._connect_donation_alerts(da_config["token"])