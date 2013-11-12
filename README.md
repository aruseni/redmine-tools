**Redmine target version creator** allows you to easily split the year into 52 automatically created separate target versions (201401, 201402 and so on).

Example:

    $ python add_target_versions.py 2014-01-26 5
    Creating version 201404
    Creating version 201405
    Creating version 201406
    Creating version 201407
    Creating version 201408

**Redmine target version shift** allows you to shift each of your tasks one version forward (starting with a given version) which is very useful in case you have tasks for a few versions ahead, but right now the plans has changed and you had to add something new in the current version (instead of the end of the plan) so you need to move everything else one version forward as you don’t want versions that consist of so many tasks that you can barely finish a half of them in time.

Example:

    $ python redmine_tv_shift.py 201347
    Shifting #2627 from 201347 to 201348
    Shifting #2584 from 201347 to 201348
    Shifting #2513 from 201347 to 201348
    Shifting #2512 from 201347 to 201348
    Shifting #2511 from 201347 to 201348
    Shifting #2487 from 201348 to 201349
    Shifting #2445 from 201348 to 201349
    Shifting #2346 from 201350 to 201351
    Shifting #2320 from 201347 to 201348
    Shifting #2272 from 201352 to 201401
    Shifting #2249 from 201350 to 201351
    Shifting #2229 from 201348 to 201349
    Shifting #2112 from 201350 to 201351
    Shifting #1752 from 201349 to 201350
    Shifting #1209 from 201351 to 201352
