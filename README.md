# memey

A django project to display memes me and my friends make

## Table structure

### meme:

| **column name**            | **type**             | **description**                              |
| -------------------------- | -------------------- | -------------------------------------------- |
| number                     | PositiveSmallInteger | actual number of the meme                    |
| declared_number            | PositiveBigInteger   | the declared number of the meme              |
| media_path                 | FilePath             | local file directory link to media           |
| media_type                 | string               | image, gif or video                          |
| media_created_at           | Date                 |                                              |
| voice_recording_path       | FilePath             | local file directory link to recording       |
| voice_recording_created_at | DateTime             | unix timecode                                |
| voice_recording_transcript | Text                 | transcription of voice recording             |
| authors                    | list of foreign keys | comma seperated list of authors              |
| season                     | PositiveSmallInteger | meme season 1,2,3 e.t.c                      |
| subseason                  | string               | irish rick and morty, daniels tooltips e.t.c |
