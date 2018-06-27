CREATE TABLE `devops_auth_module_group`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '模块组名称',
    `owner_id` INT(11) NOT NULL COMMENT 'Owner ID',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB CHARSET = utf8 COLLATE utf8_general_ci COMMENT = '系统模块组';

CREATE TABLE `devops_auth_module`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '模块名称',
    `alias` VARCHAR(255) NOT NULL COMMENT '模块别名',
    `url` VARCHAR(255) NOT NULL COMMENT 'URL',
    `owner_id` INT(11) NOT NULL COMMENT 'Owner ID',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`),
    UNIQUE `idx_url`(`url`)
) ENGINE = InnoDB CHARSET = utf8 COLLATE utf8_general_ci COMMENT = '系统模块表';

CREATE TABLE `devops_auth_module_groups`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `module_id` INT(11) NOT NULL COMMENT '模块 ID',
    `group_id` INT(11) NOT NULL COMMENT '模块组 ID',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB CHARSET = utf8 COLLATE utf8_general_ci COMMENT = '系统模块组关联表';

CREATE TABLE `devops_auth_module_permission`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) NOT NULL COMMENT '用户ID',
    `module_id` INT(11) NOT NULL COMMENT '模块 ID',
    `value` INT(3) NOT NULL COMMENT '权限值，rwx-777',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB COMMENT = '系统模块权限定义';

CREATE TABLE `devops_auth_user_group_permission`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `group_id` INT(11) NOT NULL COMMENT '用户组 ID',
    `module_id` INT(11) NOT NULL COMMENT '模块 ID',
    `value` INT(3) NOT NULL COMMENT '权限值，rwx-777',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB COMMENT = '系统用户组权限定义';

CREATE TABLE `devops_auth_module_group_permission`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `group_id` INT(11) NOT NULL COMMENT '模块组 ID',
    `value` INT(3) NOT NULL COMMENT '权限值，rwx-777',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB COMMENT = '系统模块组权限定义';

---patch
ALTER TABLE `devops_workshop_dev_web`.`devops_auth_module_groups`
ADD COLUMN `is_enabled` TINYINT(1) NOT NULL DEFAULT 1 AFTER `group_id`;

CREATE TABLE `devops_auth_module_groups_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '模user ID',
  `group_id` int(11) NOT NULL COMMENT '模块组 ID',
  `is_enabled` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='系统模块组关联表';

-- patch 2018-06-27
ALTER TABLE
    `devops_auth_module` ADD `open_db` VARCHAR(255) NULL DEFAULT NULL COMMENT '数据库名称' AFTER `url`,
    ADD `open_table` VARCHAR(255) NULL DEFAULT NULL COMMENT '数据表名称' AFTER `open_db`,
    ADD `open_id` INT NULL DEFAULT NULL COMMENT '数据记录ID' AFTER `open_table`;