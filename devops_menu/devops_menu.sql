CREATE TABLE `devops_menu_menuitem`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT 'name'  COMMENT '菜单名',
    `menu` text NULL COMMENT 'menu' COMMENT '菜单内容',
    `parent_id` INT(11) NOT NULL DEFAULT -1  COMMENT '父菜单',
    `has_sub_menu` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否有子菜单',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否启用',
    `created_by` VARCHAR(255) NOT NULL COMMENT '创建人',
    `updated_by` VARCHAR(255) NOT NULL COMMENT '最后更新人',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY(`id`)
) ENGINE = InnoDB COMMENT = '系统菜单';


--patch--

ALTER TABLE `devops_menu_menuitem`
ADD COLUMN `order_index` INT(11) NOT NULL DEFAULT 1;

update devops_menu_menuitem set order_index = id where 1  limit 1000;
