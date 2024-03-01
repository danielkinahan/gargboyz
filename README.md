# memey

A django project to display memes me and my friends make

## Table structure

### meme:

| **column name**            | **type**  | **description**                              |
| -------------------------- | --------- | -------------------------------------------- |
| media_path                 | string    | local file directory link to media           |
| media_type                 | string    | image, gif or video                          |
| media_created_at           | timestamp | unix timecode                                |
| voice_recording_path       | string    | local file directory link to recording       |
| voice_recording_created_at | timestamp | unix timecode                                |
| voice_recording_transcript | string    | transcription of voice recording             |
| authors                    | list      | comma seperated list of authors              |
| season                     | integer   | meme season 1,2,3 e.t.c                      |
| subseason                  | string    | irish rick and morty, daniels tooltips e.t.c |
