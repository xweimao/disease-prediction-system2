// 主要JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面动画
    initializeAnimations();

    // 初始化表单验证
    initializeFormValidation();

    // 初始化工具提示
    initializeTooltips();
});

function initializeAnimations() {
    // 为卡片添加淡入动画
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
}

function initializeFormValidation() {
    // 数字输入验证
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNumberInput(this);
        });

        input.addEventListener('blur', function() {
            validateNumberInput(this);
        });
    });
}

function validateNumberInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);

    if (input.value === '') {
        input.setCustomValidity('');
        return;
    }

    if (isNaN(value)) {
        input.setCustomValidity('请输入有效的数字');
    } else if (min !== undefined && value < min) {
        input.setCustomValidity(`值不能小于 ${min}`);
    } else if (max !== undefined && value > max) {
        input.setCustomValidity(`值不能大于 ${max}`);
    } else {
        input.setCustomValidity('');
    }
}

function initializeTooltips() {
    // 如果使用Bootstrap，初始化工具提示
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// 通用API请求函数
async function makeApiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// 显示加载状态
function showLoading(element, text = '加载中...') {
    const originalContent = element.innerHTML;
    element.innerHTML = `<span class="loading-spinner me-2"></span>${text}`;
    element.disabled = true;

    return function hideLoading() {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// 显示通知消息
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // 自动移除通知
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// 平滑滚动到元素
function scrollToElement(element, offset = 0) {
    const elementPosition = element.offsetTop - offset;
    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });
}

// 格式化数字
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// 验证表单
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}
