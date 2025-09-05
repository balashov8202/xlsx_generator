// DOM elements
const generateForm = document.getElementById('generateForm');
const generateBtn = document.getElementById('generateBtn');
const previewBtn = document.getElementById('previewBtn');
const progressContainer = document.getElementById('progressContainer');
const previewContainer = document.getElementById('previewContainer');
const closePreview = document.getElementById('closePreview');
const toast = document.getElementById('toast');

// Form elements
const rowCountInput = document.getElementById('rowCount');
const fileNameInput = document.getElementById('fileName');
const resumeLengthSelect = document.getElementById('resumeLength');

// Progress elements
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const recordsCount = document.getElementById('recordsCount');
const fileSize = document.getElementById('fileSize');

// Preview elements
const previewTable = document.getElementById('previewTable');

// Sample data for preview
const sampleData = [
    {
        lastName: 'Иванов',
        firstName: 'Александр',
        patronymic: 'Сергеевич',
        phone: '+7 (495) 123-45-67',
        email: 'ivanov.alex@yandex.ru',
        telegram: '@ivanov_alex',
        position: 'Разработчик Python',
        company: 'Яндекс',
        salary: '180 тыс. руб.',
        birthDate: '15.03.1985',
        comment: 'Ответственный и пунктуальный специалист',
        resume: 'Опыт разработки на Python, Django/FastAPI, SQL, тестирование и CI/CD...'
    },
    {
        lastName: 'Петрова',
        firstName: 'Мария',
        patronymic: 'Дмитриевна',
        phone: '+7 (812) 987-65-43',
        email: 'petrova.maria@mail.ru',
        telegram: '@maria_dev',
        position: 'Frontend-разработчик',
        company: 'VK',
        salary: '160 тыс. руб.',
        birthDate: '22.07.1990',
        comment: 'Быстро обучается и инициативна',
        resume: 'React/Vue, TypeScript, адаптивная верстка, оптимизация производительности...'
    },
    {
        lastName: 'Сидоров',
        firstName: 'Дмитрий',
        patronymic: 'Александрович',
        phone: '+7 (343) 555-12-34',
        email: 'sidorov.dmitry@bk.ru',
        telegram: '@dmitry_sid',
        position: 'DevOps-инженер',
        company: 'СберТех',
        salary: '200 тыс. руб.',
        birthDate: '08.11.1988',
        comment: 'Отличные коммуникативные навыки',
        resume: 'CI/CD, Docker, Kubernetes, Terraform, мониторинг и безопасность...'
    }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateFileSizeEstimate();
});

// Event listeners
function initializeEventListeners() {
    generateForm.addEventListener('submit', handleFormSubmit);
    previewBtn.addEventListener('click', showPreview);
    closePreview.addEventListener('click', hidePreview);
    
    // Update file size estimate when inputs change
    rowCountInput.addEventListener('input', updateFileSizeEstimate);
    resumeLengthSelect.addEventListener('change', updateFileSizeEstimate);
    
    // Close preview when clicking outside
    document.addEventListener('click', function(e) {
        if (previewContainer.style.display === 'block' && 
            !previewContainer.contains(e.target) && 
            !previewBtn.contains(e.target)) {
            hidePreview();
        }
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(generateForm);
    const data = {
        rowCount: parseInt(formData.get('rowCount')),
        fileName: formData.get('fileName'),
        resumeLength: formData.get('resumeLength')
    };
    
    // Validate form data
    if (data.rowCount < 100 || data.rowCount > 50000) {
        showToast('Количество записей должно быть от 100 до 50,000', 'error');
        return;
    }
    
    if (!data.fileName.trim()) {
        showToast('Введите имя файла', 'error');
        return;
    }
    
    // Show progress and start generation
    showProgress();
    generateBtn.disabled = true;
    
    try {
        await generateExcelFile(data);
    } catch (error) {
        console.error('Error generating file:', error);
        showToast('Ошибка при генерации файла: ' + error.message, 'error');
        hideProgress();
        generateBtn.disabled = false;
    }
}

// Generate Excel file
async function generateExcelFile(data) {
    const startTime = Date.now();
    
    // Simulate progress updates
    const progressInterval = setInterval(() => {
        updateProgress();
    }, 100);
    
    try {
        // Make request to Flask server
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the file as blob
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${data.fileName}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        // Show success message
        const endTime = Date.now();
        const duration = ((endTime - startTime) / 1000).toFixed(1);
        const fileSizeMB = (blob.size / (1024 * 1024)).toFixed(1);
        
        showToast(`Файл успешно создан! Размер: ${fileSizeMB} МБ, время: ${duration}с`, 'success');
        
    } finally {
        clearInterval(progressInterval);
        hideProgress();
        generateBtn.disabled = false;
    }
}

// Show progress
function showProgress() {
    progressContainer.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = 'Подготовка данных...';
    recordsCount.textContent = '0';
    fileSize.textContent = '0 МБ';
}

// Hide progress
function hideProgress() {
    progressContainer.style.display = 'none';
}

// Update progress
function updateProgress() {
    const currentWidth = parseInt(progressFill.style.width) || 0;
    if (currentWidth < 90) {
        const newWidth = Math.min(currentWidth + Math.random() * 10, 90);
        progressFill.style.width = newWidth + '%';
        
        // Update progress text
        if (newWidth < 30) {
            progressText.textContent = 'Генерация данных...';
        } else if (newWidth < 60) {
            progressText.textContent = 'Создание Excel файла...';
        } else if (newWidth < 90) {
            progressText.textContent = 'Финальная обработка...';
        }
        
        // Update stats
        const rowCount = parseInt(rowCountInput.value);
        const estimatedRecords = Math.floor((newWidth / 100) * rowCount);
        recordsCount.textContent = estimatedRecords.toLocaleString();
        
        // Estimate file size based on resume length
        const resumeLength = resumeLengthSelect.value;
        let sizeMultiplier = 1;
        if (resumeLength === 'medium') sizeMultiplier = 2;
        if (resumeLength === 'long') sizeMultiplier = 3;
        
        const estimatedSize = ((estimatedRecords * sizeMultiplier * 0.5) / 1000).toFixed(1);
        fileSize.textContent = estimatedSize + ' МБ';
    }
}

// Show preview
function showPreview() {
    previewContainer.style.display = 'block';
    renderPreviewTable();
}

// Hide preview
function hidePreview() {
    previewContainer.style.display = 'none';
}

// Render preview table
function renderPreviewTable() {
    const table = document.createElement('table');
    
    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = [
        'Фамилия', 'Имя', 'Отчество', 'Телефон', 'Email', 
        'Telegram', 'Должность', 'Компания', 'Зарплата', 
        'Дата рождения', 'Комментарий', 'Резюме'
    ];
    
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body
    const tbody = document.createElement('tbody');
    sampleData.forEach(row => {
        const tr = document.createElement('tr');
        const values = [
            row.lastName, row.firstName, row.patronymic, row.phone, row.email,
            row.telegram, row.position, row.company, row.salary,
            row.birthDate, row.comment, row.resume
        ];
        
        values.forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    
    // Clear and append table
    previewTable.innerHTML = '';
    previewTable.appendChild(table);
}

// Update file size estimate
function updateFileSizeEstimate() {
    const rowCount = parseInt(rowCountInput.value) || 10000;
    const resumeLength = resumeLengthSelect.value;
    
    let sizeMultiplier = 1;
    if (resumeLength === 'medium') sizeMultiplier = 2;
    if (resumeLength === 'long') sizeMultiplier = 3;
    
    const estimatedSize = ((rowCount * sizeMultiplier * 0.5) / 1000).toFixed(1);
    
    // Update the info display if needed
    console.log(`Estimated file size: ${estimatedSize} МБ for ${rowCount} records`);
}

// Show toast notification
function showToast(message, type = 'success') {
    const toastIcon = toast.querySelector('.toast-icon');
    const toastMessage = toast.querySelector('.toast-message');
    
    // Set icon based on type
    if (type === 'success') {
        toastIcon.className = 'toast-icon fas fa-check-circle';
        toast.className = 'toast success show';
    } else if (type === 'error') {
        toastIcon.className = 'toast-icon fas fa-exclamation-circle';
        toast.className = 'toast error show';
    }
    
    toastMessage.textContent = message;
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

// Utility functions
function formatNumber(num) {
    return num.toLocaleString('ru-RU');
}

function formatFileSize(bytes) {
    const sizes = ['Б', 'КБ', 'МБ', 'ГБ'];
    if (bytes === 0) return '0 Б';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to form groups
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const input = group.querySelector('input, select');
        if (input) {
            input.addEventListener('focus', () => {
                group.style.transform = 'translateY(-2px)';
                group.style.transition = 'transform 0.2s ease';
            });
            
            input.addEventListener('blur', () => {
                group.style.transform = 'translateY(0)';
            });
        }
    });
    
    // Add click animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add ripple effect CSS
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
