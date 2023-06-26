# TrackerPy

## What is this?

This is a Discord bot that can serve as a to-do list.
It should've had a Track functionality, while it cannot run without a `discord-py < 2.0.0`.
Maybe one day it will have a track function as well.

## Usage

### Group

The user can be joined into a group, so the task assign will applied to all members in the same group.

**Join the group**

```
!group join <group-name>
```

**Leave the group**

```
!group leave <group-name>
```

**List all groups**

```
!group list
```

**Assign task to group**

```
!group assign <group-name>
<task1>
<task2>
...
```

### Task

**New**

```
!task new
<task1>
<task2>
...
```

**Delete**

```
!task delete
<task1>
<task2>
...
```

**Done**

```
!task done
<task1>
<task2>
...
```

**Undone**

```
!task undone
<task1>
<task2>
...
```

**Archive: You CANNOT unarchived, use this command carefully**

```
!task archive
<task1>
<task2>
...
```

### Display

**Archived**

```
!task display archived
```

**Mine**

```
!task display mine
```

**users**

```
!task display users
```

### Card

Oh my god, my favorite part(what?)

```
!card <leetcode-username>
```

## How to run this app

1. Fill in those tokens, urls, keys in `.env_template`
2. Rename `.env_template` to `.env`
3. Setup supabase

```
create table
  public.group (
    id uuid not null default gen_random_uuid (),
    group_name character varying null,
    user_id character varying null,
    join_at timestamp with time zone null default now(),
    constraint group_pkey primary key (id)
  ) tablespace pg_default;
create table
  public.archived (
    id uuid not null default gen_random_uuid (),
    archived_at timestamp with time zone null default now(),
    user_id character varying null,
    task_name character varying null,
    done boolean null default false,
    constraint archived_pkey primary key (id)
  ) tablespace pg_default;
create table
  public.tasks (
    id uuid not null default gen_random_uuid (),
    user_id character varying null,
    task_name character varying null,
    created_at timestamp with time zone null default now(),
    done boolean null default false,
    constraint tasks_pkey primary key (id)
  ) tablespace pg_default;
```
