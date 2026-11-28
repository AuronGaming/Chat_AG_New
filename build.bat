@echo off
echo === Сборка Chat_AG ===
python -m PyInstaller --clean --onefile --windowed --name "Chat_AG" ^
  --collect-all PyQt6 ^
  --hidden-import "parameters.theme.themes" ^
  --hidden-import "parameters.theme.obs_overlay" ^
  --hidden-import "parameters.theme.editor.dialog" ^
  --hidden-import "parameters.theme.editor" ^
  --hidden-import "parameters.hotkeys.bindings" ^
  --hidden-import "parameters.hotkeys.quick_actions" ^
  --hidden-import "parameters.other.activation" ^
  --hidden-import "parameters.other.window_view" ^
  --hidden-import "parameters.other.about" ^
  --hidden-import "parameters.other.section" ^
  --hidden-import "parameters.general.chat" ^
  --hidden-import "parameters.general.statistics" ^
  --hidden-import "parameters.general.links_filters" ^
  --hidden-import "parameters.general.window_behavior" ^
  --hidden-import "parameters.general.description" ^
  --hidden-import "parameters.general.section" ^
  --hidden-import "parameters.general.visual" ^
  --hidden-import "parameters.sound.audio" ^
  --hidden-import "parameters.sound.description" ^
  --hidden-import "parameters.sound.events" ^
  --hidden-import "parameters.sound.section" ^
  --hidden-import "parameters.sound.visual" ^
  --hidden-import "parameters.sound.voice" ^
  --hidden-import "parameters.connections.icons" ^
  --hidden-import "parameters.connections.panel" ^
  --hidden-import "parameters.connections.registry" ^
  --hidden-import "parameters.connections.section" ^
  --hidden-import "parameters.connections.donation_alert" ^
  --hidden-import "parameters.connections.goodgame" ^
  --hidden-import "parameters.connections.kick" ^
  --hidden-import "parameters.connections.music_service" ^
  --hidden-import "parameters.connections.other_streamer" ^
  --hidden-import "parameters.connections.rutube" ^
  --hidden-import "parameters.connections.telegram" ^
  --hidden-import "parameters.connections.tiktok" ^
  --hidden-import "parameters.connections.twitch" ^
  --hidden-import "parameters.connections.vk_play" ^
  --hidden-import "parameters.connections.youtube" ^
  --hidden-import "settings_window.help_section" ^
  --hidden-import "main_screen.theme_config" ^
  --hidden-import "main_screen.close_dialog" ^
  --hidden-import "main_screen.custom_title_bar" ^
  --hidden-import "main_screen.input_panel" ^
  --hidden-import "main_screen.main_window_donations" ^
  --hidden-import "main_screen.main_window_handlers" ^
  --hidden-import "main_screen.main_window_platforms" ^
  --hidden-import "main_screen.main_window_settings" ^
  --hidden-import "main_screen.platform_icons" ^
  --hidden-import "main_screen.platform_panel" ^
  --add-data "themes;themes" ^
  --add-data "assets;assets" ^
  Chat_AG.py
echo === Готово! exe в папке dist/ ===
pause