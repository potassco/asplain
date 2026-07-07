% @label("{} is a student",(S,)) :: student(S)
% @label("{} is a course",(C,)) :: course(C)
% @label("{} is registered for {}",(S,C)) :: registered(S,C)
% @label("{} studied for {}",(S,C)) :: studied(S,C)
% @label("{} can take the exam in {}",(S,C)) :: exam_access(S,C)
% @label("{} attends the {} exam",(S,C)) :: attended_exam(S,C)
% @label("{} gets a good grade",(S,)) :: good_grade(S)
% @label("{} fails an exam",(S,)) :: fail(S)


% @label("{} can take the exam in {} because they are registered for the course",(S,C))
exam_access(S,C) :- student(S), course(C), registered(S,C).

% @label("{} gets a good grade because they registered for the exam, attended it, and studied for the course",(S,C))
good_grade(S) :- exam_access(S,C), attended_exam(S,C), studied(S,C).

% @label("{} fails because they registered for the exam, attended it but did not study for the course",(S,C))
fail(S) :- exam_access(S,C), attended_exam(S,C), not studied(S,C).

% @label("{} fails because they registered for the exam but did not attend it",(S,C))
fail(S) :- exam_access(S,C), not attended_exam(S,C).

% ----- Instance
student(alice).
student(nick).
student(paul).

course(math).
course(german).
course(biology).

registered(alice,math).
% @removable
studied(alice,math).
% @removable
attended_exam(alice,math).

registered(nick,german).
% @addable
studied(nick,german).
% @removable
attended_exam(nick,german).

registered(paul,biology).
% @removable
studied(paul,biology).
% @addable
attended_exam(paul,biology).
