# bot_kitvk
##Для игрового сервера Unturned + RocketMod##
##For game server Unturned + RocketMod##
----------------------------------------------------------------------------
**Бот для автоматического получения SteamID игроков из комментариев к обсуждению в ВК и добавления прав на игровом сервере.**

**BOT for automatically obtain SteamID players from the comments to the discussion in the VK and adding permissions to the game server.**

**Получает ссылку на профиль Steam из комментариев пользователей в обсуждении в ВК. Проверяет существование профиля Steam. Конвертирует CustomURL в SteamID64. Подключается к RCON и шлет команды "p add SteamID64 VK".**

**Gets a reference to Steam profiles from user comments in the discussion VK. Checks the existence of the Steam profile. Converts CustomURL in SteamID64. Connect to RCON and send "p add SteamID64 VK" commands.**

-----------------------------------------------------------------------------


TO DO:

-Сделать проверку уникальности VK_ID (один пользователь ВК - один добавленный SteamID)

-Сделать проверку всех добавленных ранее на выход из группы. Удалять права.

-Изменить способ передачи пароля RCON

-Запоминать и отслеживать предыдущее кол-во сообщений. Проверять только новые, а не 10 последних, как сейчас

-----------------------------------------------------------------------------

**В разработке.**
**In developing.**

I run my script as service (with systemctl command). See HowToRunAsService.txt
