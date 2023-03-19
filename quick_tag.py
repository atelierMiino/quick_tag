import argparse
import os
import workorder.work_order as wo


class ConsolePrint:
    SUCCESS     = '\033[96m[  OK  ] '
    WARNING     = '\033[93m[ WARN ] '
    FAILURE     = '\033[91m[ FAIL ] '
    ENDCOLOR    = '\033[0m'

    def print_msg( str ):
        print( f'{ str }' )

    def print_success( str ):
        print( f'{ ConsolePrint.SUCCESS }{ str }{ ConsolePrint.ENDCOLOR }' )

    def print_warning( str ):
        print( f'{ ConsolePrint.WARNING }{ str }{ ConsolePrint.ENDCOLOR }' )

    def print_failure( str ):
        print( f'{ ConsolePrint.FAILURE }{ str }{ ConsolePrint.ENDCOLOR }' )


class FileInfo:
    def __init__( self, root, file_name, full_file_path ):
        self._root = root
        self._file_name = file_name
        self._full_file_path = full_file_path

    @property
    def root( self ):
        return self._root

    @property
    def file_name( self ):
        return self._file_name

    @property
    def full_file_path( self ):
        return self._full_file_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f',
        '--filepath',
        action = 'store',
        default = './',
        help = 'Specify filepath. If not specified, current folder will be used.',
        required = False
    )
    parser.add_argument(
        '-n',
        '--tag_by_fname',
        action = 'store_true',
        default = False,
        help = 'Tag by File-Name rather than Tag by File-Folder.'
    )

    arguments = parser.parse_args()

    # Test for argument validity.
    if ( os.path.isdir( arguments.filepath ) ):
        pass
    elif ( os.path.isfile( arguments.filepath ) ):
        ConsolePrint.print_failure( f'{ arguments.filepath } is an invalid File-Folder.' )
        os.sys.exit()
    else:
        ConsolePrint.print_failure( f'{ arguments.filepath } does not exist.' )
        os.sys.exit()

    # Load all audio files to be operated on to a single array.
    all_files = []
    for root, directories, files in os.walk( arguments.filepath ):
        for file_name in files:
            full_file_path = os.path.join( root, file_name )
            current_file = FileInfo( root, file_name, full_file_path )
            all_files.append( current_file )

    ConsolePrint.print_msg( f'=======================================================\n' )

    # Initialize variables to keep track of operation statistics.
    audio_files = 0
    invalid_files = 0
    just_tagged_files = 0
    already_tagged_files = 0
    for file_info in all_files:
        ConsolePrint.print_msg( f'File found: { file_info.full_file_path }' )

        current_job = wo.WorkOrder( file_info.root, file_info.file_name, file_info.full_file_path )

        # Call correct operation.
        job_status = wo.ReturnCode.UNRESOLVED
        if ( arguments.tag_by_fname ):
            job_status = current_job.tag_by_fname()
        else:
            job_status = current_job.tag_by_ffolder()

        # Output data
        match ( job_status ):
            case wo.ReturnCode.INVALID_FILE:
                ConsolePrint.print_failure( f'File is not a compatible filetype for mutagen.' )
                invalid_files += 1
            case wo.ReturnCode.INVALID_NAME:
                ConsolePrint.print_warning( f'File name was not formatted correctly. Possible user error.' )
                audio_files += 1
            case wo.ReturnCode.SUCCESS_TAGGED:
                ConsolePrint.print_success( f'Metadata written successfully.' )
                audio_files += 1
                just_tagged_files += 1
            case wo.ReturnCode.ALREADY_TAGGED:
                ConsolePrint.print_success( f'Metadata is already correct.' )
                audio_files += 1
                already_tagged_files += 1

    # Statistics only need to be displayed if many files were operated upon.
    total_files = audio_files + invalid_files
    ConsolePrint.print_msg( '' )
    ConsolePrint.print_msg( f'QUICK-TAG STATISTICS' )
    ConsolePrint.print_msg( f'-------------------------------------------------------' )
    ConsolePrint.print_msg( f'{ audio_files }/{ total_files } files found are audio files.' )
    ConsolePrint.print_msg( f'{ just_tagged_files }/{ audio_files } audio files were just tagged.' )
    ConsolePrint.print_msg( f'{ already_tagged_files }/{ audio_files } audio files were already tagged correctly.' )