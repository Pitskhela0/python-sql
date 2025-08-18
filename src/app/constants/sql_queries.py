class SQLQueries:
    """SQL query templates"""

    CREATE_ROOMS_TABLE = """
        CREATE TABLE IF NOT EXISTS Rooms (
            room_id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """

    CREATE_STUDENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            birthday DATE NOT NULL,
            sex ENUM('M', 'F') NOT NULL,
            room_id INT,
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """

    DROP_ROOMS_TABLE = "DROP TABLE IF EXISTS Rooms"
    DROP_STUDENTS_TABLE = "DROP TABLE IF EXISTS Students"

    INSERT_ROOM_QUERY = """
        INSERT INTO Rooms (room_id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
    """

    INSERT_STUDENT_QUERY = """
        INSERT INTO Students (student_id, name, birthday, sex, room_id)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            name = VALUES(name),
            birthday = VALUES(birthday),
            sex = VALUES(sex),
            room_id = VALUES(room_id)
    """

    ROOMS_WITH_STUDENTS_COUNT = """
        SELECT Rooms.room_id, Rooms.name, count(Students.student_id) AS students_count
        FROM Rooms
        LEFT JOIN Students
        ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id;
    """

    TOP_5_LEAST_AVERAGE_AGE_ROOMS = """
        SELECT
            Rooms.room_id,
            Rooms.name,
            AVG(FLOOR(DATEDIFF(CURDATE(), Students.birthday) / 365.25)) AS avg_age
        FROM Rooms
        INNER JOIN Students ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id
        ORDER BY avg_age ASC
        LIMIT 5;
    """

    TOP_5_LARGEST_AGE_DIFF_ROOMS = """
        SELECT
            Rooms.room_id,
            Rooms.name,
            MAX(TIMESTAMPDIFF(YEAR, Students.birthday, CURDATE())) -
            MIN(TIMESTAMPDIFF(YEAR, Students.birthday, CURDATE())) AS age_diff
        FROM Rooms
        INNER JOIN Students
            ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id, Rooms.name
        ORDER BY age_diff DESC
        LIMIT 5;
    """

    ROOMS_WITH_DIFFERENT_SEX = """
        SELECT
            Rooms.room_id,
            Rooms.name
        FROM Rooms
        INNER JOIN Students
            ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id
        HAVING COUNT(DISTINCT Students.sex) > 1;
    """