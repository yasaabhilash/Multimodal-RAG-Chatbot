import { uploadFile } from "../services/upload";

function UploadBox() {

  const handleUpload =
    async (event) => {

      const files =
        event.target.files;

      if (!files.length) return;

      try {

        for (const file of files) {

          await uploadFile(file);

        }

        alert(
          "All files uploaded successfully"
        );

      } catch (error) {

        console.error(error);

        alert(
          "Upload failed"
        );

      }
    };

  return (

    <div className="upload-box">

      <h3>
        Upload Documents
      </h3>

      <input
        type="file"
        multiple
        onChange={handleUpload}
      />

    </div>

  );

}

export default UploadBox;