import os
import mutagen
import ffmpeg


class ReturnCode:
    # Mutagen could not read file.
    INVALID_FILE    = -2
    # Tag by File-Name invalid filename. See README.md
    INVALID_NAME    = -1
    # File was tagged without issue.
    SUCCESS_TAGGED  = 0
    # File was already tagged and will be unmodified.
    ALREADY_TAGGED  = 1
    # Undefined
    UNRESOLVED      = 99


class WorkOrder:
    def __init__( self, root, file_name, full_file_path ):
        self._root              = root
        self._file_name         = file_name
        self._full_file_path    = full_file_path
        # Buffer for refined artist / title data.
        self._artist_title      = [ [ '' ], [ '' ] ]

    def _replace_file( self ):
        new_file_name = self._file_name.split( '.' )[ 0 ] + '.opus'
        new_full_file_path = self._root + '/' + new_file_name

        # ffmpeg Filetype conversion.
        try:
            input_stream = ffmpeg.input( self._full_file_path )
            output_stream = ffmpeg.output( input_stream, new_full_file_path )
            output_stream.run()
        except ffmpeg.Error:
            # ffmpeg could not convert mp4 tag file. Delete inoperable opus version.
            os.remove( new_full_file_path )
            return ReturnCode.INVALID_FILE

        # Remove old file.
        os.remove( self._full_file_path )

        # Update member variables. For continuity rather than functionality.
        self._file_name = new_file_name
        self._full_file_path = new_full_file_path

        # Return new audio object for evaluation.
        new_audio_obj = mutagen.File( self._full_file_path )
        return new_audio_obj

    def _operate( self ):
        try:
            audio_obj = mutagen.File( self._full_file_path )
            # Mutagen cannot identify the filetype.
            if ( audio_obj == None ):
                return ReturnCode.INVALID_FILE
        except mutagen.MutagenError:
            # Mutagen cannot load the file it identified.
            return ReturnCode.INVALID_FILE

        # mp4 / m4a tags are annoying to deal with. Replace file using ffmpeg.
        if ( type( audio_obj.tags ) == mutagen.mp4.MP4Tags ):
            audio_obj = self._replace_file()

            if ( audio_obj == ReturnCode.INVALID_FILE ):
                return ReturnCode.INVALID_FILE

        # Compare program's artist / title with metadata artist / title.
        artist_match = False
        title_match = False

        # Mutagen will throw a KeyError if tag does not yet
        # exist and is being read.
        try:
            if audio_obj[ 'artist' ] == self._artist_title[ 0 ]:
                artist_match = True
            else:
                audio_obj[ 'artist' ] = self._artist_title[ 0 ]
        except KeyError:
            audio_obj[ 'artist' ] = self._artist_title[ 0 ]
        try:
            if audio_obj[ 'title' ] == self._artist_title[ 1 ]:
                title_match = True
            else:
                audio_obj[ 'title' ] = self._artist_title[ 1 ]
        except KeyError:
            audio_obj[ 'title' ] = self._artist_title[ 1 ]

        if ( artist_match and title_match ):
            return ReturnCode.ALREADY_TAGGED
        else:
            audio_obj.save()
            return ReturnCode.SUCCESS_TAGGED

    def tag_by_fname( self ):
        # Format the File-Name.
        stem = self._file_name.split( '.' )[ 0 ]
        split_stem = stem.split( ' - ' )

        if ( len( split_stem ) != 2 ):
            # Tag by File-Name does not work for invalid File-Names.
            return ReturnCode.INVALID_NAME
        else:
            # File-Name was correct.
            artist_title = [ split_stem[ 0 ], split_stem[ 1 ] ]

            # Populate artist_title member.
            self._artist_title = [ [ artist_title[ 0 ] ], [ artist_title[ 1 ] ] ]

            # Work on Metadata.
            return self._operate()

    def tag_by_ffolder( self ):
        file_folder = self._root.split( '/' )[ -1 ]
        stem = self._file_name.split( '.' )[ 0 ]
        artist_title = [ file_folder, stem ]

        # Populate artist_title member.
        self._artist_title = [ [ artist_title[ 0 ] ], [ artist_title[ 1 ] ] ]

        # Work on Metadata.
        return self._operate()