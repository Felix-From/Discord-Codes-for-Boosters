CREATE TABLE `code_data` (
  `id` int(11) NOT NULL,
  `code` varchar(128) NOT NULL,
  `type` int(128) NOT NULL,
  `rarity` varchar(30) NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`content`)),
  `created_at` datetime(6) NOT NULL,
  `created_from` varchar(128) NOT NULL,
  `is_used` int(2) NOT NULL,
  `is_used_at` datetime(6) NOT NULL,
  `is_used_from` varchar(128) NOT NULL,
  `is_given_to_LogID` int(128) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `code_log` (
  `id` int(11) NOT NULL,
  `discord_user_id` varchar(128) NOT NULL,
  `discord_user_name` varchar(128) NOT NULL,
  `time` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `code_id` int(128) NOT NULL,
  `code` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `code_data`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `code_log`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `code_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `code_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

COMMIT;