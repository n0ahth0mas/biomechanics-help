drop table if exists Classes;
drop table if exists Chapters;
drop table if exists Sections;
drop table if exists Questions;
drop table if exists Answers;
drop table if exists Glossary;
drop table if exists Images;
drop table if exists Videos;
drop table if exists Admin;
drop table if exists InfoSlide;

create TABLE Classes(
        className     TEXT check(className IS NOT NULL),
        classCode     TEXT check(classCode IS NOT NULL),
        UNIQUE (classCode),
        PRIMARY KEY (classCode)
);

create TABLE Chapters(
        chapterID     INTEGER,
        chapterName   TEXT check(chapterName IS NOT NULL),
        classCode       TEXT,
        PRIMARY KEY (chapterID),
        FOREIGN KEY (classCode) REFERENCES Classes(classCode)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Sections(
        sectionID     INTEGER,
        chapterID     INTEGER check(chapterID IS NOT NULL),
        sectionName   INTEGER check(sectionName IS NOT NULL),
        PRIMARY KEY (sectionID),
        FOREIGN KEY (chapterID) REFERENCES Chapters (chapterID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Questions(
        questionID    INTEGER,
        questionText  TEXT check(questionText IS NOT NULL),
        sectionID     INTEGER check(sectionID IS NOT NULL),
        chapterID     INTEGER check(chapterID IS NOT NULL),
        classCode     TEXT check(classCode IS NOT NULL),
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
        chapterID     INTEGER check(chapterID IS NOT NULL),
        classCode       TEXT check(classCode IS NOT NULL),
        PRIMARY KEY (infoSlideID),
        FOREIGN KEY (sectionID) REFERENCES Sections (sectionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE Answers(
        answerID      INTEGER,
        questionID    INTEGER,
        classID       INTEGER check(classID IS NOT NULL),
        correctness   BOOLEAN check(correctness IS NOT NULL),
        answerText    TEXT check(answerText IS NOT NULL),
        answerReason  TEXT,
        PRIMARY KEY (answerID, questionID),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
              ON UPDATE CASCADE
              ON DELETE CASCADE
);

create TABLE Glossary(
        classCode       TEXT,
        termID        INTEGER,
        term          TEXT check(term IS NOT NULL),
        definition    TEXT check(definition IS NOT NULL),
        PRIMARY KEY (classCode, termID),
        FOREIGN KEY (classCode) REFERENCES Class(classCode)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE QuestionImages(
        questionID     INTEGER,
        sectionID     INTEGER check(sectionID IS NOT NULL),
        chapterID     INTEGER check(chapterID IS NOT NULL),
        classCode       TEXT check(classCode IS NOT NULL),
        imageFile      TEXT check(imageFile IS NOT NULL),
        PRIMARY KEY (imageFile),
        FOREIGN KEY (questionID) REFERENCES Questions (questionID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

create TABLE QuestionInfoSlide(
        infoSlideID    INTEGER,
        classCode       TEXT check(classCode IS NOT NULL),
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
        classCode     TEXT,
        PRIMARY KEY (email,classCode),
        FOREIGN KEY (email) REFERENCES Users (email)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        FOREIGN KEY (classCode) REFERENCES Classes (classCode)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);
