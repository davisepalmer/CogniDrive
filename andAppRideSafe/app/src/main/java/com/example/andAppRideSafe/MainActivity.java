package com.example.android_take_photos_and_save_gallery;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import android.os.Handler;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
//import android.widget.ImageView;
import android.widget.Toast;
import android.util.Base64;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

// OKHTTP
import okhttp3.*;



public class MainActivity extends AppCompatActivity {
    Handler handler;
    Runnable runnable;
    String URL_TO_SERVER = "https://www.toptal.com/developers/postbin/1708821181498-9731337090488";
//    String URL_TO_SERVER  = "https://mintaio.com/driving";
    public static final int CAMERA_PERM_CODE = 101;
    public static final int CAMERA_REQUEST_CODE = 102;
//    ImageView selectedImage;
    Button cameraBtn;
    String currentPhotoPath;
    boolean isDriving = false;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

//        selectedImage = findViewById(R.id.displayImageView);
        cameraBtn = findViewById(R.id.cameraBtn);

        cameraBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!isDriving) {
                    startDriving();
                } else {
                    endDriving();
                }
            }
        });
    }

    private void startDriving() {
        verifyPermissions();
        handler = new Handler();
        runnable = new Runnable() {
            @Override
            public void run() {
                if (isDriving) {
                    dispatchTakePictureIntent();
                    handler.postDelayed(this, 30000); // 30sec
                }
            }
        };
        isDriving = true;
        cameraBtn.setText("End Drive");
        cameraBtn.setBackgroundColor(getResources().getColor(android.R.color.holo_red_light));
        handler.postDelayed(runnable, 0);
    }


    private void endDriving() {
        isDriving = false;
        cameraBtn.setText("Start Drive");
        cameraBtn.setBackgroundColor(getResources().getColor(android.R.color.holo_green_light));
    }


    private void verifyPermissions() {
        String[] permissions = {Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                Manifest.permission.CAMERA};

        if (ContextCompat.checkSelfPermission(this.getApplicationContext(),
                permissions[0]) == PackageManager.PERMISSION_GRANTED
                && ContextCompat.checkSelfPermission(this.getApplicationContext(),
                permissions[1]) == PackageManager.PERMISSION_GRANTED
                && ContextCompat.checkSelfPermission(this.getApplicationContext(),
                permissions[2]) == PackageManager.PERMISSION_GRANTED) {
            dispatchTakePictureIntent();
        } else {
            ActivityCompat.requestPermissions(this,
                    permissions,
                    CAMERA_PERM_CODE);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == CAMERA_PERM_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                dispatchTakePictureIntent();
            } else {
                Toast.makeText(this, "Camera Permission is Required to Use camera.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == CAMERA_REQUEST_CODE) {
            if (resultCode == Activity.RESULT_OK) {
                try {
                    final File f = new File(currentPhotoPath);
//                    selectedImage.setImageURI(Uri.fromFile(f));
                    Log.d("tag", "Absolute Url of Image is " + Uri.fromFile(f));

                    String imageBase64 = convertImageToBase64(f);

                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            OkHttpClient client = new OkHttpClient();

                            MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
                            RequestBody body = RequestBody.create(mediaType, "image=" + imageBase64);
                            Request request = new Request.Builder()
                                    .url(URL_TO_SERVER)
                                    .post(body)
                                    .addHeader("Content-Type", "application/x-www-form-urlencoded")
                                    .build();

                            try {
                                Response response = client.newCall(request).execute();
                                if (response.isSuccessful()) {
                                    String responseData = response.body().string();
                                } else {
                                    // Handle error
                                }
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }).start();

                    Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
                    Uri contentUri = Uri.fromFile(f);
                    sendBroadcast(mediaScanIntent);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private String convertImageToBase64(File imageFile) {
        try {
            FileInputStream fis = new FileInputStream(imageFile);
            byte[] imageBytes = new byte[(int) imageFile.length()];
            fis.read(imageBytes);
            fis.close();
            String base64Image = Base64.encodeToString(imageBytes, Base64.DEFAULT);
            return "data:image/jpeg;base64," + base64Image;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,
                ".jpg",
                storageDir
        );

        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {

            }
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(this,
                        "com.example.android.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, CAMERA_REQUEST_CODE);

                isDriving = true;
                cameraBtn.setText("End Drive");
                cameraBtn.setBackgroundColor(getResources().getColor(android.R.color.holo_red_light));
            }
        }
    }
}
