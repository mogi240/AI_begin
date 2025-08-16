<!DOCTYPE html>
<html lang="ko">
<head>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>여행 블로그 | 세상의 모든 여행 이야기</title>
    <meta name="description" content="AJAX와 페이지네이션으로 구현된 여행 블로그입니다. 다양한 여행 후기와 팁을 확인하세요.">
    <meta name="keywords" content="여행, 블로그, 여행 후기, 페이지네이션, 맛집, 숙소, 여행 팁">
    <meta name="author" content="김치군">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "여행 블로그",
      "description": "다양한 여행 정보를 제공하는 개인 블로그입니다.",
      "url": "https://www.your-blog-url.com",
      "potentialAction": {
        "@type": "SearchAction",
        "query-input": "required name=query",
        "target": "https://www.your-blog-url.com/search?q={query}"
      }
    }
    </script>

    <style>
        /* 기본 스타일링 */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background-color: #FFFFFF; /* 배경색을 흰색으로 변경 */
            color: #212529;
            line-height: 1.6;
        }
        header {
            background-color: #FFFFFF;
            color: #212529;
            padding: 40px 20px;
            text-align: center;
            border-bottom: 1px solid #dee2e6;
        }
        header h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        header p {
            margin-top: 5px;
            font-size: 1.2rem;
            opacity: 0.9;
        }

        /* 전체 컨테이너 및 레이아웃 */
        .container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }
        main {
            display: flex;
            gap: 20px;
        }
        .content {
            flex: 3;
        }
        .sidebar {
            flex: 1;
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            box-shadow: none; /* 우측 트리메뉴의 세로선 역할을 하는 그림자 제거 */
            max-width: 300px;
        }
        @media (max-width: 768px) {
            main {
                flex-direction: column;
            }
            .sidebar {
                max-width: 100%;
            }
        }

        /* 게시글 카드 스타일 */
        .post-card {
            background-color: #FFFFFF;
            border-radius: 0;
            box-shadow: none;
            border-bottom: 1px solid #ddd;
            margin-bottom: 0;
            padding: 20px 0;
            transition: background-color 0.2s;
            cursor: pointer;
        }
        .post-card:last-child {
            border-bottom: none;
        }
        .post-card:hover {
            background-color: #F8F9FA;
        }
        .post-card h2 {
            margin-top: 0;
            color: #212529;
        }
        .post-card p {
            color: #495057;
        }

        /* 카드 내용 (텍스트 + 이미지) 정렬 */
        .card-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-direction: row-reverse;
        }
        .text-content {
            flex-grow: 1;
        }
        .post-thumbnail {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
        }
        .post-date {
            font-size: 0.9em;
            color: #6c757d;
            margin-top: 15px;
        }

        /* 페이지네이션 스타일 */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
            padding: 10px;
            background-color: #FFFFFF;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .pagination button {
            text-decoration: none;
            color: #4CAF50;
            padding: 8px 12px;
            margin: 0 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
            transition: background-color 0.3s, color 0.3s;
            background-color: #FFFFFF;
            cursor: pointer;
        }
        .pagination button:hover {
            background-color: #f0f2f5;
            color: #4CAF50;
            border-color: #4CAF50;
        }
        .pagination button.active {
            background-color: #B2E7C3;
            color: #000000;
            border-color: #B2E7C3;
            font-weight: bold;
            cursor: default;
        }
        .pagination button:disabled {
            color: #CCCCCC;
            cursor: not-allowed;
            background-color: #FFFFFF;
        }
        
        /* 트리 메뉴 스타일 */
        .sidebar h3 {
            margin-top: 0;
            color: #212529;
            margin-bottom: 15px;
        }
        .sidebar ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .sidebar li {
            margin: 5px 0;
        }
        .sidebar a {
            text-decoration: none;
            color: #212529;
            display: block;
            padding: 8px 10px;
            border-radius: 5px;
            transition: background-color 0.2s;
        }
        .sidebar a:hover {
            background-color: #e9ecef;
        }
        .menu-item {
            cursor: pointer;
            position: relative;
        }
        /* + 아이콘 스타일 */
        .menu-item.has-children > a.menu-toggle::before {
            content: '+';
            font-family: Arial, sans-serif;
            margin-right: 8px;
            transition: transform 0.2s;
            display: inline-block;
        }
        /* - 아이콘 스타일 (활성화 시) */
        .menu-item.has-children.active > a.menu-toggle::before {
            content: '-';
            transform: rotate(0deg);
        }
        ul.submenu {
            padding-left: 20px;
            display: none;
        }
        ul.submenu.active {
            display: block;
        }
        .menu-item a.leaf-node {
            padding-left: 15px;
            font-weight: normal;
            color: #495057;
        }
        .menu-item a.leaf-node:hover {
            background-color: #E6F5EC;
            color: #4CAF50;
        }

        /* 글 상세 페이지 스타일 */
        #post-detail-container {
            width: 100%;
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .detail-card h2 {
            color: #212529;
            font-size: 2rem;
            margin-bottom: 15px;
            text-align: center;
        }
        .detail-card img {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .detail-card p {
            color: #495057;
            font-size: 1.1em;
            line-height: 1.8;
            margin-bottom: 10px;
        }
        .detail-card #detail-date {
            font-size: 0.9em;
            color: #6c757d;
            text-align: right;
            border-top: 1px solid #dee2e6;
            padding-top: 10px;
            margin-top: 20px;
        }
        .back-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
            font-size: 1em;
            transition: background-color 0.3s;
        }
        .back-button:hover {
            background-color: #45a049;
        }

        /* 댓글 섹션 스타일 */
        #comments-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
        }
        #comments-section h3 {
            color: #212529;
            margin-bottom: 20px;
        }
        #comments-list {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            min-height: 80px;
            margin-bottom: 20px;
        }
        .comment-card {
            background-color: #FFFFFF;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .comment-card strong {
            color: #495057;
            font-size: 0.95em;
        }
        .comment-card .comment-content {
            margin: 5px 0 10px;
            color: #343a40;
        }
        .comment-card .comment-date {
            font-size: 0.8em;
            color: #adb5bd;
            text-align: right;
        }
        /* 댓글 수정/삭제 버튼 컨테이너 */
        .comment-actions {
            text-align: right;
            margin-top: 10px;
        }
        .comment-actions button {
            background-color: #6c757d; /* 회색 버튼 */
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.85em;
            margin-left: 5px;
            transition: background-color 0.2s;
        }
        .comment-actions button:hover {
            background-color: #5a6268;
        }
        .comment-actions .delete-comment-btn {
            background-color: #dc3545; /* 빨간색 삭제 버튼 */
        }
        .comment-actions .delete-comment-btn:hover {
            background-color: #c82333;
        }


        /* 댓글 폼 스타일 */
        .comment-form {
            background-color: #FFFFFF;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #dee2e6;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
        }
        .comment-form h4 {
            margin-top: 0;
            color: #212529;
            margin-bottom: 15px;
        }
        .comment-form div {
            margin-bottom: 15px;
        }
        .comment-form label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #495057;
        }
        .comment-form input[type="text"],
        .comment-form input[type="password"], /* 암호 필드 추가 */
        .comment-form textarea {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 1em;
            color: #495057;
        }
        .comment-form textarea {
            min-height: 80px;
            resize: vertical;
        }
        .comment-form .submit-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s;
            float: right;
        }
        .comment-form .submit-button:hover {
            background-color: #45a049;
        }
        .comment-form::after {
            content: "";
            display: table;
            clear: both;
        }

        /* 푸터 스타일 */
        footer {
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            background-color: #343a40;
            color: white;
        }
    </style>

</head>
<body>

    <header>
        <h1>여행 블로그</h1>
        <p>세상의 모든 여행 이야기</p>
    </header>

    <main class="container">
        <!-- 메인 콘텐츠 영역 (게시글 목록 및 상세 페이지) -->
        <div class="content">
            <!-- 글 목록 영역 -->
            <div id="list-view-content">
                <h2>최신 게시글</h2>
                <div id="posts-container">
                    <p>게시글을 불러오는 중입니다...</p>
                </div>
                <div id="pagination-container" class="pagination"></div>
            </div>

            <!-- 글 상세 페이지 영역 -->
            <div id="post-detail-container" style="display: none;">
                <button id="back-to-list-btn" class="back-button">목록으로</button>
                <div class="detail-card">
                    <h2 id="detail-title"></h2>
                    <img id="detail-thumbnail" class="post-thumbnail" alt="Post Thumbnail">
                    <p id="detail-content"></p>
                    <p id="detail-date"></p>
                </div>

                <!-- 댓글 섹션 -->
                <div id="comments-section">
                    <h3>댓글</h3>
                    <div id="comments-list">
                        <p>댓글을 불러오는 중...</p>
                    </div>

                    <div class="comment-form">
                        <h4>댓글 작성</h4>
                        <div>
                            <label for="comment-author">작성자:</label>
                            <input type="text" id="comment-author" placeholder="이름을 입력하세요">
                        </div>
                        <div>
                            <label for="comment-content">내용:</label>
                            <textarea id="comment-content" placeholder="댓글을 입력하세요"></textarea>
                        </div>
                        <div>
                            <label for="comment-password">암호:</label>
                            <input type="password" id="comment-password" placeholder="암호를 입력하세요">
                        </div>
                        <button id="comment-submit-btn" class="submit-button">댓글 등록</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 사이드바 및 트리 메뉴 영역 -->
        <aside class="sidebar">
            <h3>카테고리</h3>
            <ul id="tree-menu-container" class="tree-menu">
                <p>메뉴를 불러오는 중입니다...</p>
            </ul>
        </aside>
    </main>

    <footer>
        <p>&copy; 2024 여행 블로그. All rights reserved.</p>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const postsContainer = document.getElementById('posts-container');
            const paginationContainer = document.getElementById('pagination-container');
            const treeMenuContainer = document.getElementById('tree-menu-container');
            const listViewContent = document.getElementById('list-view-content');
            const postDetailContainer = document.getElementById('post-detail-container');
            const backToListBtn = document.getElementById('back-to-list-btn');

            const detailTitle = document.getElementById('detail-title');
            const detailThumbnail = document.getElementById('detail-thumbnail');
            const detailContent = document.getElementById('detail-content');
            const detailDate = document.getElementById('detail-date');

            const commentsList = document.getElementById('comments-list');
            const commentAuthorInput = document.getElementById('comment-author');
            const commentContentInput = document.getElementById('comment-content');
            const commentPasswordInput = document.getElementById('comment-password'); // 암호 입력 필드
            const commentSubmitBtn = document.getElementById('comment-submit-btn');

            const postsPerPage = 10;
            let currentPage = 1;
            let currentPostId = null;
            let selectedCategory = {
                step1: '',
                step2: '',
                step3: '',
                step4: ''
            };
            let postsDataCache = [];

            /**
             * @brief 서버에서 넘어오는 /Date(timestamp)/ 형식의 문자열을 포맷팅합니다.
             * @param {string} dateValue - 서버에서 넘어온 날짜 문자열
             * @returns {string} YYYY-MM-DD HH:mm 또는 현지 날짜 형식의 문자열
             */
            function formatServerDate(dateValue) {
                const datePattern = /\/Date\((\d+)\)\//;
                const match = dateValue.match(datePattern);
                
                if (match) {
                    const timestamp = parseInt(match[1]);
                    const date = new Date(timestamp);
                    const year = date.getFullYear();
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const day = String(date.getDate()).padStart(2, '0');
                    const hours = String(date.getHours()).padStart(2, '0');
                    const minutes = String(date.getMinutes()).padStart(2, '0');
                    return `${year}-${month}-${day} ${hours}:${minutes}`;
                } else {
                    const date = new Date(dateValue);
                    if (!isNaN(date.getTime())) {
                        return date.toLocaleDateString();
                    } else {
                        return '날짜 형식 오류';
                    }
                }
            }


            /**
             * @brief 게시글을 화면에 렌더링하는 함수 (목록 보기)
             * @param {Array} postsToDisplay - 렌더링할 게시글 객체들의 배열입니다.
             */
            function renderPosts(postsToDisplay) {
                postsContainer.innerHTML = '';
                postsDataCache = postsToDisplay;

                if (postsToDisplay.length === 0) {
                    postsContainer.innerHTML = '<p>표시할 게시글이 없습니다.</p>';
                    return;
                }

                postsToDisplay.forEach(post => {
                    const postCard = document.createElement('div');
                    postCard.classList.add('post-card');
                    postCard.dataset.postId = post.Seq;
                    
                    postCard.addEventListener('click', () => {
                        showPostDetail(post.Seq);
                    });

                    const cardContent = document.createElement('div');
                    cardContent.classList.add('card-content');
                    
                    const image = document.createElement('img');
                    image.src = "http://127.0.0.1/Images/image_1.jpg";
                    image.alt = post.Title; 
                    image.classList.add('post-thumbnail');
                    cardContent.appendChild(image);

                    const textContent = document.createElement('div');
                    textContent.classList.add('text-content');
                    
                    const title = document.createElement('h2');
                    title.textContent = post.Title;

                    const content = document.createElement('p');
                    content.textContent = post.Content ? post.Content.substring(0, 150) + '...' : ''; 
                    
                    const regDate = document.createElement('p');
                    regDate.classList.add('post-date');

                    if (post.regDate) {
                        regDate.textContent = `등록일: ${formatServerDate(post.regDate)}`;
                    }

                    textContent.appendChild(title);
                    textContent.appendChild(content);
                    textContent.appendChild(regDate);
                    cardContent.appendChild(textContent);
                    postCard.appendChild(cardContent);
                    postsContainer.appendChild(postCard);
                });
            }

            /**
             * @brief 페이지네이션 UI를 화면에 렌더링하는 함수
             * @param {number} totalPages - 전체 페이지 수
             */
            function renderPagination(totalPages) {
                paginationContainer.innerHTML = '';
                
                const currentBlock = Math.ceil(currentPage / 10);
                const startPage = (currentBlock - 1) * 10 + 1;
                const endPage = Math.min(startPage + 9, totalPages);

                const prevButton = document.createElement('button');
                prevButton.textContent = '이전';
                if (currentPage <= 1) {
                    prevButton.disabled = true;
                } else {
                    prevButton.addEventListener('click', () => {
                        currentPage = startPage - 1; 
                        fetchPostsData();
                    });
                }
                paginationContainer.appendChild(prevButton);

                for (let i = startPage; i <= endPage; i++) {
                    const pageButton = document.createElement('button');
                    pageButton.textContent = i;
                    pageButton.classList.add('page-btn');
                    
                    if (i === currentPage) {
                        pageButton.classList.add('active');
                    }

                    pageButton.addEventListener('click', () => {
                        currentPage = i;
                        fetchPostsData();
                    });
                    paginationContainer.appendChild(pageButton);
                }

                const nextButton = document.createElement('button');
                nextButton.textContent = '다음';
                if (currentPage >= totalPages) {
                    nextButton.disabled = true;
                } else {
                    nextButton.addEventListener('click', () => {
                        currentPage = endPage + 1;
                        fetchPostsData();
                    });
                }
                paginationContainer.appendChild(nextButton);
            }
            
            /**
             * @brief 서버로부터 게시글 데이터를 가져오고 화면을 업데이트하는 메인 함수
             */
            function fetchPostsData() {
                postsContainer.innerHTML = '<p>게시글을 불러오는 중입니다...</p>';
                paginationContainer.innerHTML = '';

                let requestData = {
                    page: currentPage,
                    rows: postsPerPage
                };

                if (selectedCategory.step1) requestData['단계1'] = selectedCategory.step1;
                if (selectedCategory.step2) requestData['단계2'] = selectedCategory.step2;
                if (selectedCategory.step3) requestData['단계3'] = selectedCategory.step3;
                if (selectedCategory.step4) requestData['단계4'] = selectedCategory.step4;

                $.ajax({
                    url: `http://localhost/data_json/GetPosts`,
                    type: 'GET',
                    dataType: 'json',
                    data: requestData,
                    success: function(response) {
                        renderPosts(response.data);
                        renderPagination(response.totalPages);
                    },
                    error: function(xhr, status, error) {
                        console.error('데이터를 불러오는 중 오류 발생:', status, error);
                        postsContainer.innerHTML = `<p>게시글을 불러오는 데 실패했습니다. 잠시 후 다시 시도해주세요.</p>`;
                        paginationContainer.innerHTML = '';
                    }
                });
            }

            /**
             * @brief 트리 메뉴 데이터를 계층 구조로 변환하는 함수
             * @param {Array} flatData - 서버에서 받아온 평탄한 메뉴 데이터
             * @returns {Object} 계층 구조로 변환된 메뉴 데이터
             */
            function buildHierarchicalMenu(flatData) {
                const menu = {};
                flatData.forEach(item => {
                    let currentLevel = menu;
                    if (item.Step1) {
                        if (!currentLevel[item.Step1]) currentLevel[item.Step1] = {};
                        currentLevel = currentLevel[item.Step1];
                    }
                    if (item.Step2) {
                        if (!currentLevel[item.Step2]) currentLevel[item.Step2] = {};
                        currentLevel = currentLevel[item.Step2];
                    }
                    if (item.Step3) {
                        if (!currentLevel[item.Step3]) currentLevel[item.Step3] = {};
                        currentLevel = currentLevel[item.Step3];
                    }
                    if (item.Step4) {
                        if (!currentLevel[item.Step4]) currentLevel[item.Step4] = {};
                    }
                });
                return menu;
            }

            /**
             * @brief 계층 구조 메뉴 데이터를 HTML 리스트로 렌더링하는 재귀 함수
             * @param {Object} menuData - 계층 구조 메뉴 데이터
             * @param {HTMLElement} parentElement - 메뉴를 추가할 부모 DOM 요소
             * @param {Array} currentPath - 현재까지의 메뉴 경로 (필터링에 사용)
             */
            function renderTreeMenu(menuData, parentElement, currentPath = []) {
                const ul = document.createElement('ul');
                ul.classList.add('submenu');
                parentElement.appendChild(ul);
                for (const key in menuData) {
                    const li = document.createElement('li');
                    const newPath = [...currentPath, key];
                    const hasChildren = Object.keys(menuData[key]).length > 0;
                    const anchor = document.createElement('a');
                    anchor.textContent = key;
                    anchor.href = "#";
                    if (hasChildren) {
                        li.classList.add('menu-item', 'has-children');
                        anchor.classList.add('menu-toggle');
                    } else {
                        anchor.classList.add('leaf-node');
                    }
                    
                    anchor.addEventListener('click', (e) => {
                        e.preventDefault();
                        let pathLength = newPath.length;
                        selectedCategory = {
                            step1: pathLength >= 1 ? newPath[0] : 'NOT',
                            step2: pathLength >= 2 ? newPath[1] : 'NOT',
                            step3: pathLength >= 3 ? newPath[2] : 'NOT',
                            step4: pathLength >= 4 ? newPath[3] : 'NOT'
                        };
                        currentPage = 1;
                        fetchPostsData();
                    });
                    
                    li.appendChild(anchor);
                    ul.appendChild(li);

                    if (hasChildren) {
                        renderTreeMenu(menuData[key], li, newPath);
                    }
                }
            }

            /**
             * @brief 서버로부터 트리 메뉴 데이터를 가져와 렌더링하는 함수
             */
            function loadTreeMenu() {
                treeMenuContainer.innerHTML = '<p>메뉴를 불러오는 중입니다...</p>';
                $.ajax({
                    url: `http://localhost/data_json/GetTreeMenu`,
                    type: 'GET',
                    dataType: 'json',
                    success: function(response) {
                        treeMenuContainer.innerHTML = '';
                        const hierarchicalMenu = buildHierarchicalMenu(response);
                        const topLevelUl = document.createElement('ul');
                        topLevelUl.classList.add('tree-menu');

                        for (const step1Key in hierarchicalMenu) {
                            const li1 = document.createElement('li');
                            li1.classList.add('menu-item', 'has-children');
                            const a1 = document.createElement('a');
                            a1.textContent = step1Key;
                            a1.href = "#";
                            a1.classList.add('menu-toggle');
                            
                            a1.addEventListener('click', (e) => {
                                e.preventDefault();
                                selectedCategory = {
                                    step1: step1Key,
                                    step2: 'NOT',
                                    step3: 'NOT',
                                    step4: 'NOT'
                                };
                                currentPage = 1;
                                fetchPostsData();
                            });
                            
                            li1.appendChild(a1);
                            topLevelUl.appendChild(li1);
                            renderTreeMenu(hierarchicalMenu[step1Key], li1, [step1Key]);
                        }
                        treeMenuContainer.appendChild(topLevelUl);
                        const menuToggles = treeMenuContainer.querySelectorAll('.menu-toggle');
                        menuToggles.forEach(toggle => {
                            const parentLi = toggle.closest('li.menu-item');
                            const submenu = parentLi.querySelector('ul.submenu');
                            toggle.addEventListener('click', (e) => {
                                e.preventDefault();
                                if (submenu) {
                                    submenu.classList.toggle('active');
                                    parentLi.classList.toggle('active');
                                }
                            });
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error('트리 메뉴 데이터를 불러오는 중 오류 발생:', status, error);
                        treeMenuContainer.innerHTML = `<p>메뉴를 불러오는 데 실패했습니다.</p>`;
                    }
                });
            }

            /**
             * @brief 캐시된 데이터에서 특정 게시글을 찾아 상세 내용을 표시
             * @param {number} postId - 조회할 게시글의 고유 ID (Seq)
             */
            function showPostDetail(postId) {
                currentPostId = postId;
                const post = postsDataCache.find(p => p.Seq === postId);

                if (post) {
                    listViewContent.style.display = 'none';
                    postDetailContainer.style.display = 'block';

                    detailTitle.textContent = post.Title;
                    detailThumbnail.src = "http://127.0.0.1/Images/image_1.jpg";
                    detailThumbnail.alt = post.Title;
                    detailContent.textContent = post.Content;
                    if (post.regDate) {
                        detailDate.textContent = `등록일: ${formatServerDate(post.regDate)}`;
                    }
                    loadComments(postId);
                } else {
                    alert('게시글 상세 데이터를 다시 불러옵니다.');
                    detailTitle.textContent = '게시글을 찾을 수 없습니다.';
                    detailContent.textContent = '';
                    commentsList.innerHTML = '<p>댓글을 불러올 수 없습니다.</p>';
                }
            }
            
            /**
             * @brief 글 목록 화면을 보여주고 상세 페이지를 숨기는 함수
             */
            function hidePostDetail() {
                postDetailContainer.style.display = 'none';
                listViewContent.style.display = 'block';
                renderPosts(postsDataCache); 
            }

            /**
             * @brief 특정 게시글의 댓글을 불러와 화면에 렌더링하는 함수
             * @param {number} postId - 댓글을 불러올 게시글의 ID (댓글 테이블의 글ID와 매핑)
             */
            function loadComments(postId) {
                commentsList.innerHTML = '<p>댓글을 불러오는 중...</p>';
                $.ajax({
                    url: `http://localhost/data_json/GetComments?글ID=${postId}`,
                    type: 'GET',
                    dataType: 'json',
                    success: function(response) {
                        commentsList.innerHTML = '';
                        if (response && response.length > 0) {
                            response.forEach(comment => {
                                const commentCard = document.createElement('div');
                                commentCard.classList.add('comment-card');
                                commentCard.dataset.commentId = comment.seq;

                                const authorElem = document.createElement('strong');
                                authorElem.textContent = comment.작성자;

                                const contentElem = document.createElement('p');
                                contentElem.classList.add('comment-content');
                                contentElem.textContent = comment.내용;

                                const dateElem = document.createElement('p');
                                dateElem.classList.add('comment-date');
                                if (comment.등록일자) {
                                    dateElem.textContent = formatServerDate(comment.등록일자);
                                }

                                const actionsDiv = document.createElement('div');
                                actionsDiv.classList.add('comment-actions');

                                const editButton = document.createElement('button');
                                editButton.textContent = '수정';
                                editButton.classList.add('edit-comment-btn');
                                editButton.addEventListener('click', () => {
                                    const newContent = prompt('수정할 내용을 입력하세요:', comment.내용);
                                    if (newContent !== null) { // 사용자가 취소하지 않았다면
                                        const password = prompt('댓글 암호를 입력하세요:');
                                        if (password) {
                                            updateComment(comment.seq, comment.작성자, newContent, password);
                                        } else {
                                            alert('암호를 입력해야 수정할 수 있습니다.');
                                        }
                                    }
                                });

                                const deleteButton = document.createElement('button');
                                deleteButton.textContent = '삭제';
                                deleteButton.classList.add('delete-comment-btn');
                                deleteButton.addEventListener('click', () => {
                                    if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
                                        const password = prompt('댓글 암호를 입력하세요:');
                                        if (password) {
                                            deleteCommentFunc(comment.seq, password);
                                        } else {
                                            alert('암호를 입력해야 삭제할 수 있습니다.');
                                        }
                                    }
                                });

                                actionsDiv.appendChild(editButton);
                                actionsDiv.appendChild(deleteButton);

                                commentCard.appendChild(authorElem);
                                commentCard.appendChild(contentElem);
                                commentCard.appendChild(dateElem);
                                commentCard.appendChild(actionsDiv);
                                commentsList.appendChild(commentCard);
                            });
                        } else {
                            commentsList.innerHTML = '<p>아직 댓글이 없습니다. 첫 댓글을 남겨주세요!</p>';
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('댓글을 불러오는 중 오류 발생:', status, error);
                        commentsList.innerHTML = '<p>댓글을 불러오는 데 실패했습니다.</p>';
                    }
                });
            }

            /**
             * @brief 새로운 댓글을 등록하는 함수
             */
            function addComment() {
                const author = commentAuthorInput.value.trim();
                const content = commentContentInput.value.trim();
                const password = commentPasswordInput.value.trim(); // 암호 값 가져오기

                if (!author || !content || !password) {
                    alert('작성자, 내용, 암호를 모두 입력해주세요.');
                    return;
                }

                if (!currentPostId) {
                    alert('현재 게시글 ID를 알 수 없습니다.');
                    return;
                }

                $.ajax({
                    url: `http://localhost/data_json/AddComment`,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        글ID: currentPostId,
                        작성자: author,
                        내용: content,
                        글쓰기암호: password // 암호 데이터 전송
                    },
                    success: function(response) {
                        if (response.success) {
                            alert(response.message);
                            commentAuthorInput.value = '';
                            commentContentInput.value = '';
                            commentPasswordInput.value = ''; // 암호 입력란 초기화
                            loadComments(currentPostId);
                        } else {
                            alert('댓글 등록 실패: ' + response.message);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('댓글 등록 중 오류 발생:', status, error);
                        alert('댓글 등록 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
                    }
                });
            }

            /**
             * @brief 댓글을 수정하는 함수
             * @param {number} seq - 수정할 댓글의 고유 ID (seq)
             * @param {string} author - 수정할 작성자 이름 (여기서는 변경하지 않고 기존 값 전달)
             * @param {string} content - 수정할 댓글 내용
             * @param {string} password - 댓글 수정 권한 확인을 위한 암호
             */
            function updateComment(seq, author, content, password) {
                $.ajax({
                    url: `http://localhost/data_json/UpdateComment`,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        seq: seq,
                        작성자: author,
                        내용: content,
                        글쓰기암호: password
                    },
                    success: function(response) {
                        if (response.success) {
                            alert(response.message);
                            loadComments(currentPostId); // 댓글 목록 새로고침
                        } else {
                            alert('댓글 수정 실패: ' + response.message);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('댓글 수정 중 오류 발생:', status, error);
                        alert('댓글 수정 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
                    }
                });
            }

            /**
             * @brief 댓글을 삭제하는 함수
             * @param {number} seq - 삭제할 댓글의 고유 ID (seq)
             * @param {string} password - 댓글 삭제 권한 확인을 위한 암호
             */
            function deleteCommentFunc(seq, password) {
                $.ajax({
                    url: `http://localhost/data_json/DeleteComment`,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        seq: seq,
                        글쓰기암호: password
                    },
                    success: function(response) {
                        if (response.success) {
                            alert(response.message);
                            loadComments(currentPostId); // 댓글 목록 새로고침
                        } else {
                            alert('댓글 삭제 실패: ' + response.message);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('댓글 삭제 중 오류 발생:', status, error);
                        alert('댓글 삭제 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
                    }
                });
            }

            // 이벤트 리스너 연결
            backToListBtn.addEventListener('click', hidePostDetail);
            commentSubmitBtn.addEventListener('click', addComment);
            
            // 페이지 로드 시 초기 데이터 및 메뉴 로드
            fetchPostsData();
            loadTreeMenu();
        });
    </script>
</body>
</html>
