
-- Articles TABLE

CREATE TABLE Articles
(
	Id INT PRIMARY KEY IDENTITY(1, 1),
	Title VARCHAR(MAX),
	Url VARCHAR(MAX),
	Category VARCHAR(500),
	Main_Photo VARCHAR(500),
	Content VARCHAR(MAX),
	Keywords VARCHAR(500),
	Posted_at DATETIME,
	Rank INT,
	Website VARCHAR(50)
);

-- Target Keywords TABLE

CREATE TABLE TargetKeywords
(
	Id INT PRIMARY KEY IDENTITY(1, 1),
	Name VARCHAR(50)
);

-- INSERT INTO TargetKeywords (Name) VALUES ('telefon'), ('post'), ('operator'), ('internet'), ('siguri kiberbetike'), ('sulm kibernetik'), ('kibernetik');