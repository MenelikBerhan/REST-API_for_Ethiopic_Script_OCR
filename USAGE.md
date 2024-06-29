## Usage

### Register a User

#### Request

`POST /user/register`

```bash
curl -X 'POST' \
  'http://localhost:8000/user/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "menelik@shoa.live",
  "password": "angolala",
  "username": "menelikBerhan",
  "full_name": "Menelik Berahan z Ethiopia"
}'
```
### Response

```bash
 content-length: 215 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:08:35 GMT 
 server: uvicorn 

 {
  "id": "660f24e4fea54f8bc6eecda7",
  "created_at": "2024-04-04T22:08:36.926180Z",
  "updated_at": "2024-04-04T22:08:36.926191Z",
  "username": "menelikBerhan",
  "email": "menelik@shoa.live",
  "full_name": "Menelik Berahan z Ethiopia"
}
```

### Login a User

#### Request

`POST /user/login`

```bash
curl -X 'POST' \
  'http://localhost:8000/user/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=menelikBerhan&password=angolala&scope=&client_id=&client_secret='
```
### Response

```bash
 content-length: 176 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:11:10 GMT 
 server: uvicorn 

 {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc",
  "token_type": "bearer"
}
```

### Get current User

#### Request

`GET /user/me`

```bash
curl -X 'GET' \
  'http://localhost:8000/user/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 213 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:12:59 GMT 
 server: uvicorn 

 {
  "id": "660f24e4fea54f8bc6eecda7",
  "created_at": "2024-04-04T22:08:36.378000",
  "updated_at": "2024-04-04T22:08:36.378000",
  "username": "menelikBerhan",
  "email": "menelik@shoa.live",
  "full_name": "Menelik Berahan z Ethiopia"
}
```

### Create an Image

#### Request

`POST /image/`

```bash
curl -X 'POST' \
  'http://localhost:8000/image/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image_properties={
  "description": "Sample page from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ]
}' \
  -F 'tesseract_config={
  "config_vars": {
    "load_system_dawg": 0,
    "preserve_interword_spaces": 1
  },
  "language": "amh-old",
  "oem": 1,
  "psm": 3
}' \
  -F 'file=@amh-test.png;type=image/png'
```
### Response

```bash
content-length: 257 
content-type: application/json 
date: Thu,04 Apr 2024 22:15:45 GMT 
server: uvicorn 

{
  "id": "660f2692fea54f8bc6eecda8",
  "created_at": "2024-04-04T22:15:46.293190Z",
  "updated_at": "2024-04-04T22:15:46.293204Z",
  "description": "Sample page from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ],
  "name": "amh-test.png",
  "ocr_finished": false
}
```

### Get List of Images

#### Request

`GET /image/`

```bash
curl -X 'GET' \
  'http://localhost:8000/image/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 1623 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:17:42 GMT 
 server: uvicorn

 {
  "images": [
    {
      "id": "660f2692fea54f8bc6eecda8",
      "created_at": "2024-04-04T22:15:46.293000",
      "updated_at": "2024-04-04T22:15:53.103000",
      "description": "Sample page from amharic-amharic dictionary",
      "ocr_output_formats": [
        "str",
        "txt"
      ],
      "name": "amh-test.png",
      "ocr_finished": true,
      "image_size": [
        644,
        560
      ],
      "image_format": "PNG",
      "image_mode": "RGB",
      "tess_config_id": "660f2693fea54f8bc6eecda9",
      "tess_output_id": "660f2698fea54f8bc6eecdaa",
      "ocr_accuracy": 80.91,
      "ocr_result_text": "\n\nመግቢያ \n\nኸሪ ልጆች! ልጆች! እንጫወት በጣም \nከእንግዲህ ልጅነት ተመልሶ አይመጣም \nልጅነቴ! ልጅነቴ፤ ማርና ወተቴ \n\nልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ \nእይልም። ፄ \nመጽሐፈ ምሣሌ 11፡16 \n\n... \n. \n\nዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት \n\nነብዩ መሐመድ (ሰ.አ.ወ) \n\n.. \n\nልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም \nእሱ ያስታውሰዋል \nየቻይናዎች አባባል \n. \n.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ \nገድለ ክርሰቶስ ሰምራ \n,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ \nሪደርስ ዳይጀሰት \n. \nለንፁሃን ሁሉም ነገር ንፁህ ነው› \nየአረቦች ምሣሊ \n.ሥ. \nልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ \nካህሊል ጊብራል \n\n "
    }
  ]
}
```

### Get List of Finished OCR Output Formats for an Image

#### Request

`GET /ocr/image/done/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/done/660f2692fea54f8bc6eecda8' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 13 
content-type: application/json 
date: Thu,04 Apr 2024 22:19:17 GMT 
server: uvicorn

[
  "str",
  "txt"
]
```

### Get OCR Result of an Image

#### Request in string (str) format

`GET /ocr/image/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/660f2692fea54f8bc6eecda8?format=str&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 1165 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:21:02 GMT 
 server: uvicorn

 "\n\nመግቢያ \n\nኸሪ ልጆች! ልጆች! እንጫወት በጣም \nከእንግዲህ ልጅነት ተመልሶ አይመጣም \nልጅነቴ! ልጅነቴ፤ ማርና ወተቴ \n\nልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ \nእይልም። ፄ \nመጽሐፈ ምሣሌ 11፡16 \n\n... \n. \n\nዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት \n\nነብዩ መሐመድ (ሰ.አ.ወ) \n\n.. \n\nልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም \nእሱ ያስታውሰዋል \nየቻይናዎች አባባል \n. \n.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ \nገድለ ክርሰቶስ ሰምራ \n,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ \nሪደርስ ዳይጀሰት \n. \nለንፁሃን ሁሉም ነገር ንፁህ ነው› \nየአረቦች ምሣሊ \n.ሥ. \nልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ \nካህሊል ጊብራል \n\n "
```

#### Request in plain text file (txt) format

`GET /ocr/image/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/660f2692fea54f8bc6eecda8?format=txt&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-disposition: attachment; filename="amh-test_ocr-result.txt" 
content-length: 1127 
content-type: text/plain; charset=utf-8 
date: Thu,04 Apr 2024 22:22:19 GMT 
etag: "aad385818e384e7a3c070bf65d80eea9" 
last-modified: Thu,04 Apr 2024 22:15:53 GMT 
server: uvicorn

መግቢያ 

ኸሪ ልጆች! ልጆች! እንጫወት በጣም 
ከእንግዲህ ልጅነት ተመልሶ አይመጣም 
ልጅነቴ! ልጅነቴ፤ ማርና ወተቴ 

ልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ 
እይልም። ፄ 
መጽሐፈ ምሣሌ 11፡16 

... 
. 

ዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት 

ነብዩ መሐመድ (ሰ.አ.ወ) 

.. 

ልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም 
እሱ ያስታውሰዋል 
የቻይናዎች አባባል 
. 
.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ 
ገድለ ክርሰቶስ ሰምራ 
,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ 
ሪደርስ ዳይጀሰት 
. 
ለንፁሃን ሁሉም ነገር ንፁህ ነው› 
የአረቦች ምሣሊ 
.ሥ. 
ልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ 
ካህሊል ጊብራል 
```

### Create a PDF

#### Request

`POST /pdf/`

```bash
curl -X 'POST' \
  'http://localhost:8000/pdf/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc' \
  -H 'Content-Type: multipart/form-data' \
  -F 'pdf_properties={
  "description": "Sample pages from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ]
}' \
  -F 'tesseract_config={
  "config_vars": {
    "load_system_dawg": 0,
    "preserve_interword_spaces": 1
  },
  "language": "amh-old",
  "oem": 1,
  "psm": 3
}' \
  -F 'file=@desta.pdf;type=application/pdf'
```
### Response

```bash
content-length: 255 
content-type: application/json 
date: Thu,04 Apr 2024 22:25:24 GMT 
server: uvicorn

{
  "id": "660f28d4fea54f8bc6eecdab",
  "created_at": "2024-04-04T22:25:24.644697Z",
  "updated_at": "2024-04-04T22:25:24.644705Z",
  "description": "Sample pages from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ],
  "name": "desta.pdf",
  "ocr_finished": false
}
```

### Get List of PDFs

#### Request

`GET /pdf/`

```bash
curl -X 'GET' \
  'http://localhost:8000/pdf/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 10616 
content-type: application/json 
date: Thu,04 Apr 2024 22:26:25 GMT 
server: uvicorn

{
  "pdfs": [
    {
      "id": "660f28d4fea54f8bc6eecdab",
      "created_at": "2024-04-04T22:25:24.644000",
      "updated_at": "2024-04-04T22:26:14.406000",
      "description": "Sample pages from amharic-amharic dictionary",
      "ocr_output_formats": [
        "str",
        "txt"
      ],
      "name": "desta.pdf",
      "ocr_finished": true,
      "pdf_version": "1.7",
      "no_pages": 2,
      "file_size": "676660 bytes",
      "page_size": "841.92 x 1190.52 pts (A3)",
      "producer": "Microsoft: Print To PDF",
      "tess_config_id": "660f2693fea54f8bc6eecda9",
      "tess_output_id": "660f2906fea54f8bc6eecdac",
      "ocr_accuracy": {
        "1": 90.64,
        "2": 89.95
      },
      "ocr_result_text": {
        "1": "\n\nመቅድም ። \n\nፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም \nረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ \nጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። \n\n፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ \nደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ \nጠየቀ ፡ ይኾናል ። \n\nቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ \nየጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ \nጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ \nመዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ \nዳባዲ ፡ ይሻላል ። \n\n፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ \nከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ \nሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ \nዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ \nወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ \nየሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ \nስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ \nከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ \nወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። \n\n፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ \nየትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ \nዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ \nይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ \nይበዛል ። \n\nባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ \nያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ \nጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ \nወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል \nኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ \nየማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል \nቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። \n\nይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ \nየራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ \nግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ \nያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። \n\nበንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ \nቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ \nግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ \nረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። ",
        "2": "\n\nአ መቅድም ። \n\nየፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ \nነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። \n\nግ ጥም ። \n\nየጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ \nለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። \nመምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ \nበታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። \nጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ \nምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ \nምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። \nአሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ \nየትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። \nዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ \nበትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ \nየሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ \nበአ ፡ ነበርና ፡ የሚዥምረው 1፤ \nለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ \nኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። \n\nኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ \nስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ \nነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። \n\nባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ \nየሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። \n\nበግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ \nቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ \nጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ \nልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ \nየሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ \nደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ \nየሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። \nይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ \nምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ \nንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ \nዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ \nመኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ \nእስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ \nግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ \nበጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። "
      }
    }
  ]
}
```

### Get List of Finished OCR Output Formats for a PDF

#### Request

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/done/660f28d4fea54f8bc6eecdab' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 13 
content-type: application/json 
date: Thu,04 Apr 2024 22:27:20 GMT 
server: uvicorn

[
  "str",
  "txt"
]
```

### Get OCR Result of a PDF

#### Request in string format

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/660f28d4fea54f8bc6eecdab?format=str&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 10072 
content-type: application/json 
date: Thu,04 Apr 2024 22:28:05 GMT 
server: uvicorn

{
  "1": "\n\nመቅድም ። \n\nፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም \nረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ \nጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። \n\n፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ \nደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ \nጠየቀ ፡ ይኾናል ። \n\nቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ \nየጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ \nጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ \nመዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ \nዳባዲ ፡ ይሻላል ። \n\n፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ \nከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ \nሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ \nዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ \nወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ \nየሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ \nስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ \nከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ \nወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። \n\n፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ \nየትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ \nዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ \nይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ \nይበዛል ። \n\nባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ \nያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ \nጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ \nወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል \nኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ \nየማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል \nቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። \n\nይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ \nየራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ \nግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ \nያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። \n\nበንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ \nቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ \nግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ \nረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። ",
  "2": "\n\nአ መቅድም ። \n\nየፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ \nነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። \n\nግ ጥም ። \n\nየጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ \nለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። \nመምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ \nበታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። \nጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ \nምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ \nምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። \nአሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ \nየትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። \nዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ \nበትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ \nየሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ \nበአ ፡ ነበርና ፡ የሚዥምረው 1፤ \nለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ \nኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። \n\nኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ \nስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ \nነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። \n\nባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ \nየሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። \n\nበግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ \nቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ \nጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ \nልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ \nየሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ \nደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ \nየሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። \nይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ \nምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ \nንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ \nዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ \nመኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ \nእስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ \nግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ \nበጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። "
}
```

#### Request in plain text file (txt) format

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/660f28d4fea54f8bc6eecdab?format=txt&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-disposition: attachment; filename="desta_ocr-result.txt" 
content-length: 10005 
content-type: text/plain; charset=utf-8 
date: Thu,04 Apr 2024 22:29:21 GMT 
etag: "6e38d051831dd5d56e08affbf486422f" 
last-modified: Thu,04 Apr 2024 22:26:14 GMT 
server: uvicorn 


መቅድም ። 

ፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም 
ረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ 
ጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። 

፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ 
ደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ 
ጠየቀ ፡ ይኾናል ። 

ቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ 
የጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ 
ጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ 
መዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ 
ዳባዲ ፡ ይሻላል ። 

፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ 
ከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ 
ሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ 
ዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ 
ወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ 
የሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ 
ስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ 
ከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ 
ወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። 

፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ 
የትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ 
ዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ 
ይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ 
ይበዛል ። 

ባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ 
ያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ 
ጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ 
ወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል 
ኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ 
የማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል 
ቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። 

ይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ 
የራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ 
ግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ 
ያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። 

በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ 
ቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ 
ግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ 
ረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። 
					--- Page 1 ---


አ መቅድም ። 

የፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ 
ነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። 

ግ ጥም ። 

የጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ 
ለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። 
መምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ 
በታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። 
ጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ 
ምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ 
ምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። 
አሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ 
የትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። 
ዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ 
በትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ 
የሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ 
በአ ፡ ነበርና ፡ የሚዥምረው 1፤ 
ለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ 
ኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። 

ኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ 
ስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ 
ነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። 

ባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ 
የሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። 

በግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ 
ቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ 
ጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ 
ልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ 
የሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ 
ደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ 
የሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። 
ይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ 
ምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ 
ንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ 
ዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ 
መኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ 
እስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ 
ግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ 
በጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። 
					--- Page 2 ---
```
