const nums = document.querySelectorAll('.num');
const form = document.querySelector('form');
const btn = document.querySelector('.button-19');
btn.addEventListener('click', () => form.submit());
nums.forEach((num, index) => {
  num.dataset.id = index;

  num.addEventListener('keyup', () => {
    if (num.value.length == 2) {
      nums[parseInt(num.dataset.id) + 1].focus();
    }
  });
});
