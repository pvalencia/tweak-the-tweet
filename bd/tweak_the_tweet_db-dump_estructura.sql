-- phpMyAdmin SQL Dump
-- version 3.3.2deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 20-07-2010 a las 15:18:52
-- Versión del servidor: 5.1.41
-- Versión de PHP: 5.3.2-1ubuntu4.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `tweak_the_tweet_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweets`
--

CREATE TABLE IF NOT EXISTS `tweets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(200) DEFAULT NULL,
  `author` varchar(40) DEFAULT NULL,
  `tweet_id` varchar(20) DEFAULT NULL,
  `source` varchar(40) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `parsed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3993 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweets_matched`
--

CREATE TABLE IF NOT EXISTS `tweets_matched` (
  `request_id` varchar(20) NOT NULL,
  `response_id` varchar(20) NOT NULL,
  `id_match` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`id_match`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweets_parsed`
--

CREATE TABLE IF NOT EXISTS `tweets_parsed` (
  `id_tweet` int(11) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `category` varchar(40) NOT NULL DEFAULT '',
  `info` varchar(40) DEFAULT NULL,
  `contact` varchar(40) DEFAULT NULL,
  `location` varchar(40) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id_tweet`,`category`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
