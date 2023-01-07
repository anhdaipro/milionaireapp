from django.test import TestCase

# Create your tests here.

Câu 47: Vận động viên đứng đầu danh sách 100 vận động viên Việt Nam tiêu biểu
của năm 2010 là vận động viên Vũ Thị Hương của môn thể thao nào?

Câu 48: Truyện “Vợ chồng A Phủ” trong tập truyện Tây Bắc của nhà văn Tô Hoài
viết về người dân tộc nào?

Câu 49: Quốc gia nào giữ chức chủ tịch luân phiên Liên minh châu Âu trong nửa
đầu năm 2011?

Câu 50: Bánh pía là đặc sản có nguồn gốc từ tỉnh nào?
A. Bến Tre
B. Sóc Trăng
C. Bạc Liêu
D. Hậu Giang
questions=[
{"question":"Tập hợp các số thực được ký hiệu bằng chữ cái nào?",
"choice":[
    "N (Số tự nhiên)",
    "Z (Số nguyên)",
    "Q (Số hữu tỷ)",
    "R (Số thực)",
    ],
"answer":"R (Số thực)"},
{"question":"Việt Nam đã đăng cai cuộc thi sắc đẹp nào trong năm 2010?",
"choice":[
    "Hoa hậu thế giới",
"Hoa hậu Trái Đất",
"Hoa hậu hoàn vũ",
"Hoa hậu quốc tế",
],
"answer":" Hoa hậu Trái Đất"},
{"question":"Nguyên mẫu của nhân vật Hoàng Kim trong bộ phim “Bí thư tỉnh uỷ” của đạo diễn Trần Quốc Trọng là bí thư của tỉnh (cũ) nào?",
"choice":[
   "Vĩnh Phúc",
"Hải Hưng",
"Bắc Thái",
"Phú Khánh",
    ],
"answer":"Vĩnh Phúc"},
{"question":"Khí nào chiếm 80% thành phần không khí?",
"choice":[
   "N2",
"O2",
"H2",
"Cl2",
    ],
"answer":"N2"},
{"question":"Loài hoa nào được chọn là Quốc hoa của Việt Nam?",
"choice":[
    "Hoa sen",
"Hoa mai",
"Hoa đào",
"Hoa hồng",
    ],
"answer":"Hoa sen"},
{"question":"Bộ phim “The Social Network” về mạng xã hội nào đã đạt giải Quả cầu vàng 2011?",
"choice":[
    "Facebook",
"Twitter",
"Yahoo Plus",
"Opera",
],
"answer":"Facebook"},
{"question":"Vận động viên đứng đầu danh sách 100 vận động viên Việt Nam tiêu biểu của năm 2010 là vận động viên Vũ Thị Hương của môn thể thao nào?",
"choice":[
    "Điền kinh",
"Cờ vua",
"Karatedo",
"Cầu lông",
    ],
"answer":"Điền kinh"},
{"question":"Truyện “Vợ chồng A Phủ” trong tập truyện Tây Bắc của nhà văn Tô Hoài viết về người dân tộc nào?",
"choice":[
    "Vân Kiều",
"Thái",
"H’Mông",
"Tày",
    ],
"answer":"H’Mông"},
{"question":"Quốc gia nào giữ chức chủ tịch luân phiên Liên minh châu Âu trong nửa đầu năm 2011?",
"choice":[
    "Hungary",
"Bungary",
"Romania",
"Ucraikne",
    ],
"answer":"Hungary"},
{"question":"Bánh pía là đặc sản có nguồn gốc từ tỉnh nào?",
"choice":[
    "Bến Tre",
"Sóc Trăng",
"Bạc Liêu",
"Hậu Giang",
    ],
"answer":"Sóc Trăng"},
]
item=Question(question=question['question'],choice=question['choice'],level=1,answer=question['answer'])
...     list_questions.append(item)

Question.objects.bulk_create(list_questions)