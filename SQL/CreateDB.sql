create table employees
(
    EmployeeID int auto_increment
        primary key,
    Name       varchar(100) null,
    Position   varchar(100) null,
    Salary     int          null,
    Age        int          null,
    Gender     tinyint      null comment '0为男, 1为女'
);

create table attendance
(
    AttendanceID       int auto_increment
        primary key,
    EmployeeID         int      null,
    AttendanceDateTime datetime null,
    AttendanceType     tinyint  null comment '0为签到, 1为签退',
    constraint attendance_ibfk_1
        foreign key (EmployeeID) references employees (EmployeeID)
            on delete cascade
);

create trigger AddFacialInfoAfterInsert
    after insert
    on employees
    for each row
BEGIN
    INSERT INTO faceinfo (EmployeeID, Name, Face_Info)
    VALUES (NEW.EmployeeID, NEW.Name, NULL); -- 将 Face_info 设置为空
END;

create trigger DeleteAttendanceAndFacialInfoAfterDelete
    after delete
    on employees
    for each row
BEGIN
    -- 删除对应的考勤信息
    DELETE FROM Attendance WHERE EmployeeID = OLD.EmployeeID;
    -- 删除对应的人脸信息
    DELETE FROM faceinfo WHERE EmployeeID = OLD.EmployeeID;
END;

create trigger UpdateFacialInfoAfterUpdate
    after update
    on employees
    for each row
BEGIN
    UPDATE faceinfo
    SET Name = NEW.Name
    WHERE EmployeeID = NEW.EmployeeID;
END;

create trigger add_user_after_employee_insert
    after insert
    on employees
    for each row
BEGIN
    INSERT INTO user (userId, password, userType)
    VALUES (NEW.employeeId, '123456', 0);
END;

create trigger delete_user_after_employee_delete
    after delete
    on employees
    for each row
BEGIN
    DELETE FROM user WHERE userId = OLD.employeeId;
END;

create table faceinfo
(
    EmployeeID int           not null
        primary key,
    Name       varchar(100)  null,
    Face_Info  varchar(3072) null,
    constraint faceinfo_ibfk_1
        foreign key (EmployeeID) references employees (EmployeeID)
            on delete cascade
);

create table user
(
    userID   int         not null
        primary key,
    Password varchar(32) not null,
    userType tinyint     null comment '0为普通用户, 1为管理员用户',
    constraint fk_employeeId
        foreign key (userID) references employees (EmployeeID)
            on delete cascade
);

