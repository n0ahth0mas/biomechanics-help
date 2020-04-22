drop table if exists Classes;
drop table if exists Chapters;
drop table if exists Sections;
drop table if exists Questions;
drop table if exists SectionBlock;
drop table if exists Answers;
drop table if exists DropBoxes;
drop table if exists Glossary;
drop table if exists SectionImages;
drop table if exists Videos;
drop table if exists Enroll;
drop table if exists School;
drop table if exists Users;
drop table if exists User_roles;
drop table if exists Roles;

create TABLE Classes(
        className     TEXT check(className IS NOT NULL),
        classID     TEXT check(classID IS NOT NULL),
        PRIMARY KEY (classID)
);

create TABLE Chapters(
        chapterID     INTEGER,
        chapterName   TEXT check(chapterName IS NOT NULL),
        classID     TEXT check(classID IS NOT NULL),
        orderNo      INTEGER ,
        publish     BOOLEAN,
        PRIMARY KEY (chapterID),
        FOREIGN KEY (classID) REFERENCES Classes(classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Sections(
        sectionID     INTEGER,
        chapterID     INTEGER check(chapterID IS NOT NULL),
        sectionName   TEXT check(sectionName IS NOT NULL),
        orderNo         INTEGER,
        publish     BOOLEAN,
        PRIMARY KEY (sectionID),
        FOREIGN KEY (chapterID) REFERENCES Chapters (chapterID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Questions(
        questionID    INTEGER,
        questionText  TEXT check(questionText IS NOT NULL),
        sectionID     INTEGER check(sectionID IS NOT NULL),
        questionType  TEXT check(questionType IS NOT NULL),
        orderNo       INTEGER,
        imageFile     TEXT,
        PRIMARY KEY (questionID),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE SectionBlock(
        sectionBlockID    INTEGER,
        sectionText  TEXT,
        sectionID     INTEGER check(sectionID IS NOT NULL),
        orderNo         INTEGER,
        PRIMARY KEY (sectionBlockID),
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
        imageFile     TEXT,
        xposition       INTEGER,
        yposition       INTEGER,
        dropBoxHeightAdjustment   INTEGER,
        dropBoxWidthAdjustment INTEGER,
        dropBoxColor    TEXT,
        PRIMARY KEY (answerID),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
              ON UPDATE CASCADE
              ON DELETE CASCADE
);

create TABLE DragBoxes(
        dragBoxID       INTEGER,
        questionID        INTEGER,
        xposition       TEXT,
        yposition       TEXT,
        correctness     BOOLEAN check(correctness IS NOT NULL),
        imageFile       TEXT,
        PRIMARY KEY (dragBoxID),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

create TABLE Glossary(
        classID       TEXT,
        termID        INTEGER,
        term          TEXT check(term IS NOT NULL),
        definition    TEXT check(definition IS NOT NULL),
        PRIMARY KEY (termID),
        FOREIGN KEY (classID) REFERENCES Classes(classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE GlossaryImages(
        termID    INTEGER check(termID IS NOT NULL),
        imageFile      TEXT check(imageFile IS NOT NULL),
        PRIMARY KEY (termID,imageFile),
        FOREIGN KEY (termID) REFERENCES Glossary (termID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE SectionBlockImages(
        sectionBlockID    INTEGER check(sectionBlockID IS NOT NULL),
        imageFile      TEXT check(imageFile IS NOT NULL),
        xposition       TEXT check(xposition IS NOT NULL),
        yposition       TEXT check(yposition IS NOT NULL),
        PRIMARY KEY (sectionBlockID,imageFile),
        FOREIGN KEY (sectionBlockID) REFERENCES SectionBlock (sectionBlockID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Videos(
        sectionID      INTEGER check(sectionID IS NOT NULL),
        videoFile      TEXT check(videoFile IS NOT NULL),
        PRIMARY KEY (sectionID,videoFile),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);


CREATE TABLE Enroll(
        email      TEXT,
        classID    TEXT,
        lastSectionID INTEGER,
        PRIMARY KEY (email,classID),
        FOREIGN KEY (email) REFERENCES Users (email)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        FOREIGN KEY (classID) REFERENCES Classes (classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        FOREIGN KEY (lastSectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE NO ACTION
);

CREATE TABLE School(
        schoolID       TEXT,
        schoolName     TEXT,
        PRIMARY KEY(schoolID)
);

CREATE TABLE Users(
        email           TEXT,
        password        TEXT,
        name            TEXT,
        PRIMARY KEY(email)
);

CREATE TABLE User_roles(
        id              INTEGER,
        user_id         TEXT,
        role_id         INTEGER,
        PRIMARY KEY(id),
        FOREIGN KEY (user_id) REFERENCES Users (email)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        FOREIGN KEY (role_id) REFERENCES Roles (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE Roles(
        id          TEXT,
        name        TEXT,
        PRIMARY KEY(id)
);