SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema enti
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `enti` DEFAULT CHARACTER SET utf8 ;
USE `enti` ;

-- -----------------------------------------------------
-- Table `enti`.`EntityType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`EntityType` (
  `id` INT NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enti`.`Entity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`Entity` (
  `id` VARCHAR(128) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `type` INT NOT NULL,
  `canonical` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  INDEX `entity_type_idx` (`type` ASC),
  CONSTRAINT `entity_type`
    FOREIGN KEY (`type`)
    REFERENCES `enti`.`EntityType` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enti`.`ArityType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`ArityType` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enti`.`AttributeType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`AttributeType` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enti`.`Attribute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`Attribute` (
  `id` VARCHAR(128) NOT NULL,
  `required` TINYINT NOT NULL DEFAULT 0,
  `arity` INT NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `display_name` VARCHAR(128) NULL,
  `description` VARCHAR(256) NULL,
  `type` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `description_UNIQUE` (`description` ASC),
  INDEX `arity_idx` (`arity` ASC),
  INDEX `type_idx` (`type` ASC),
  CONSTRAINT `arity`
    FOREIGN KEY (`arity`)
    REFERENCES `enti`.`ArityType` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`type`)
    REFERENCES `enti`.`AttributeType` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enti`.`EntityAttribute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `enti`.`EntityAttribute` (
  `id` VARCHAR(128) NOT NULL,
  `entity_id` VARCHAR(128) NOT NULL,
  `attribute_id` VARCHAR(128) NOT NULL,
  `key` VARCHAR(128) NOT NULL,
  `value` VARCHAR(1024) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `entity_id_idx` (`entity_id` ASC),
  INDEX `attribute_id_idx` (`attribute_id` ASC),
  CONSTRAINT `entity_id`
    FOREIGN KEY (`entity_id`)
    REFERENCES `enti`.`Entity` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `attribute_id`
    FOREIGN KEY (`attribute_id`)
    REFERENCES `enti`.`Attribute` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
