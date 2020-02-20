drop table if exists Class;
drop table if exists Chapters;
drop table if exists Sections;
drop table if exists Questions;
drop table if exists Answers;
drop table if exists Glossary;
drop table if exists Images;
drop table if exists Videos;
drop table if exists Admin;

create TABLE Class(
        classID       INTEGER PRIMARY KEY,
        className     TEXT check(className IS NOT NULL),
        classCode     TEXT check(classCode IS NOT NULL),
        UNIQUE (classCode)
);

create TABLE Chapters(
        chapterID     INTEGER,
        chapterName   TEXT check(chapterName IS NOT NULL),
        classID       INTEGER,
        PRIMARY KEY (chapterID, classID),
        FOREIGN KEY (classID) REFERENCES Class(classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Sections(
        sectionID     INTEGER,
        chapterID     INTEGER check(chapterID),
        sectionName   INTEGER check(sectionName IS NOT NULL),
        PRIMARY KEY (sectionID, chapterID),
        FOREIGN KEY (chapterID) REFERENCES Chapters (chapterID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Questions(
        questionID    INTEGER,
        questionText  TEXT check(questionText IS NOT NULL),
        sectionID     INTEGER check(sectionID IS NOT NULL),
        questionType  TEXT check(questionType IS NOT NULL),
        PRIMARY KEY (questionID, sectionID),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Answers(
        answerID      INTEGER,
        questionID    INTEGER,
        correctness   BOOLEAN check(correctness IS NOT NULL),
        answerText    TEXT check(answerText IS NOT NULL),
        answerReason  TEXT,
        PRIMARY KEY (answerID, questionID),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
              ON UPDATE CASCADE
              ON DELETE CASCADE
);

create TABLE Glossary(
        classID       INTEGER,
        termID        INTEGER,
        term          TEXT check(term IS NOT NULL),
        definition    TEXT check(definition IS NOT NULL),
        PRIMARY KEY (classID, termID),
        FOREIGN KEY (classID) REFERENCES Class(classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Images(
        questionID     INTEGER,
        infoSlideID    INTEGER,
        imageFile      TEXT check(imageFile IS NOT NULL),
        PRIMARY KEY (imageFile),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Videos(
        sectionID      INTEGER,
        videoFile      TEXT check(videoFile IS NOT NULL),
        PRIMARY KEY (videoFile),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE Admin(
        upsID				   INTEGER PRIMARY KEY,
        firstName 	   TEXT check(firstName IS NOT NULL),
        lastName		   TEXT check(lastName IS NOT NULL),
        middleName	   TEXT,
        password		   TEXT check(password IS NOT NULL),
        email				   TEXT check(email IS NOT NULL)
);
