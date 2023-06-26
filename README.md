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
!group list <group-name>
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
