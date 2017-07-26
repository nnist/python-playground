def download(self, url, show_status=True):
    """
    Download a file from the given url.
    Show a progress indicator for the download status.
    Based on: http://stackoverflow.com/a/15645088/1547223
    """
    import os
    import sys
    import requests

    file_name = url.split('/')[-1]
    file_path = os.path.join(self.data_directory, file_name)

    # Do not download the data if it already exists
    if os.path.exists(file_path):
        self.logger.info('File is already downloaded')
        return file_path

    with open(file_path, 'wb') as open_file:
        print('Downloading %s' % file_name)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            # No content length header
            open_file.write(response.content)
        else:
            download = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                download += len(data)
                open_file.write(data)
                if show_status:
                    done = int(50 * download / total_length)
                    sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

return file_path

def extract(self, file_path):
    """
    Extract a tar file at the specified file path.
    """
    import os
    import tarfile

    dir_name = os.path.split(file_path)[-1].split('.')[0]

    extracted_file_directory = os.path.join(
        self.data_directory,
        dir_name
    )

    # Do not extract if the extracted directory already exists
    if os.path.isdir(extracted_file_directory):
        return False

    self.logger.info('Starting file extraction')

    def track_progress(members):
        for member in members:
            # this will be the current file being extracted
            yield member
            print('Extracting {}'.format(member.path))

    with tarfile.open(file_path) as tar:
        tar.extractall(path=self.data_directory, members=track_progress(tar))

    self.logger.info('File extraction complete')

return True
