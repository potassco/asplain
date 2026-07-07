# Final Exams

<!-- --8<-- [start:description] -->

The final exams example encoding is a simple ASP encoding with variables.
It models a university scenario with three students enrolled in different courses. 
Students who are registered for a course are allowed to take its exam. 
A student receives a good grade if they are registered, attend the exam, and study for the course. 
Otherwise, they fail either because they did not study or because they did not attend the exam.

<!-- --8<-- [end:description] -->

## Usage

<!-- --8<-- [start:usage] -->

Explanation:

```bash
asplain examples/exams/encoding.lp 1 --query "good_grade(paul)"
```

```bash
asplain examples/exams/encoding.lp 1 --nl-query "Why didn't Paul get a good grade?"
```

<!-- --8<-- [end:usage] -->
