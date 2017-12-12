
DROP TABLE IF EXISTS `course_schedule`;
CREATE TABLE `course_schedule` (
  `course_id` varchar(16) NOT NULL,
  `course_year` varchar(20) DEFAULT NULL,
  `course_term` varchar(5) DEFAULT NULL,
  `course_teacher` varchar(10) DEFAULT NULL,
  `course_place` varchar(20) DEFAULT NULL,
  `course_day` varchar(5) NOT NULL,
  `course_num` varchar(10) NOT NULL,
  `course_start_week` varchar(5) DEFAULT NULL,
  `course_end_week` varchar(5) DEFAULT NULL,
  `course_odd_dual_bool` tinyint(1) DEFAULT '0',
  `course_odd_dual` varchar(5) DEFAULT NULL
);

-- ----------------------------
--  Table structure for `courses_info`
-- ----------------------------
DROP TABLE IF EXISTS `courses_info`;
CREATE TABLE `courses_info` (
  `course_id` varchar(16) NOT NULL,
  `course_name` varchar(50) DEFAULT NULL,
  `course_nature` varchar(10) DEFAULT NULL,
  `course_credit` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
);

-- ----------------------------
--  Table structure for `grades_table`
-- ----------------------------
DROP TABLE IF EXISTS `grades_table`;
CREATE TABLE `grades_table` (
  `course_id` varchar(16) NOT NULL,
  `grade_year` varchar(20) NOT NULL,
  `grade_term` varchar(2) NOT NULL,
  `grade_point` int(10) DEFAULT NULL,
  `grade_regular` varchar(5) DEFAULT NULL,
  `grade_midterm` varchar(5) DEFAULT NULL,
  `grade_finalexam` varchar(5) DEFAULT NULL,
  `grade_total` varchar(5) DEFAULT NULL
);

-- ----------------------------
--  Table structure for `login_info`
-- ----------------------------
DROP TABLE IF EXISTS `login_info`;
CREATE TABLE `login_info` (
  `stu_id` varchar(16) NOT NULL,
  `stu_passwd` varchar(256) DEFAULT NULL,
  `login_time` date DEFAULT NULL,
  PRIMARY KEY (`stu_id`)
);

-- ----------------------------
--  Table structure for `stu_info`
-- ----------------------------
DROP TABLE IF EXISTS `stu_info`;
CREATE TABLE `stu_info` (
  `stu_id` varchar(16) NOT NULL,
  `stu_name` varchar(20) NOT NULL,
  `stu_sex` varchar(4) DEFAULT NULL,
  `stu_birth` date DEFAULT NULL,
  `stu_province` varchar(20) DEFAULT NULL,
  `stu_college` varchar(100) DEFAULT NULL,
  `stu_major` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`stu_id`)
);

