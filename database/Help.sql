drop table if exists Classes;
drop table if exists Chapters;
drop table if exists Sections;
drop table if exists Questions;
drop table if exists InfoSlide;
drop table if exists Answers;
drop table if exists Glossary;
drop table if exists QuestionImages;
drop table if exists InfoSlideImages;
drop table if exists Videos;
drop table if exists Enroll;
drop table if exists School;

create TABLE Classes(
        className     TEXT check(className IS NOT NULL),
        classID     TEXT check(classID IS NOT NULL),
        PRIMARY KEY (classID)
);

create TABLE Chapters(
        chapterID     INTEGER,
        chapterName   TEXT check(chapterName IS NOT NULL),
        classID     TEXT check(classID IS NOT NULL),
        PRIMARY KEY (chapterID),
        FOREIGN KEY (classID) REFERENCES Classes(classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Sections(
        sectionID     INTEGER,
        chapterID     INTEGER check(chapterID IS NOT NULL),
        sectionName   INTEGER check(sectionName IS NOT NULL),
        PRIMARY KEY (chapterID,sectionID),
        FOREIGN KEY (chapterID) REFERENCES Chapters (chapterID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Questions(
        questionID    INTEGER,
        questionText  TEXT check(questionText IS NOT NULL),
        sectionID     INTEGER check(sectionID IS NOT NULL),
        questionType  TEXT check(questionType IS NOT NULL),
        PRIMARY KEY (questionID),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE InfoSlide(
        infoSlideID    INTEGER,
        infoSlideText  TEXT check(infoSlideText IS NOT NULL),
        sectionID     INTEGER check(sectionID IS NOT NULL),
        PRIMARY KEY (infoSlideID),
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
        PRIMARY KEY (answerID),
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

create TABLE QuestionImages(
        questionID     INTEGER,
        imageFile      TEXT check(imageFile IS NOT NULL),
        PRIMARY KEY (imageFile),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE InfoSlideImages(
        infoSlideID    INTEGER,
        imageFile      TEXT check(imageFile IS NOT NULL),
        PRIMARY KEY (imageFile),
        FOREIGN KEY (infoSlideID) REFERENCES InfoSlide (infoSlideID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Videos(
        sectionID      INTEGER check(sectionID),
        videoFile      TEXT check(videoFile IS NOT NULL),
        PRIMARY KEY (videoFile),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);


CREATE TABLE Enroll(
        email      TEXT,
        classID    TEXT,
        PRIMARY KEY (email,classID),
        FOREIGN KEY (email) REFERENCES Users (email)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        FOREIGN KEY (classID) REFERENCES Classes (classID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
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