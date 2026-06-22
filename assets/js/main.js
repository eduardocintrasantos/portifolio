(function () {
  'use strict';

  const header = document.getElementById('header');
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav__link');
  const sections = document.querySelectorAll('section[id]');
  const contactForm = document.getElementById('contact-form');

  /* Header scroll effect */
  function onScroll() {
    header.classList.toggle('scrolled', window.scrollY > 20);
    updateActiveNav();
  }

  /* Active nav link on scroll */
  function updateActiveNav() {
    const scrollPos = window.scrollY + 100;

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach((link) => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  }

  /* Mobile menu toggle */
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.classList.toggle('open', isOpen);
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  /* Close menu on link click */
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  /* Contact form validation */
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('name');
      const email = document.getElementById('email');
      const message = document.getElementById('message');
      const successMsg = document.getElementById('form-success');

      let valid = true;

      clearErrors();

      if (!name.value.trim()) {
        showError('name', 'Informe seu nome.');
        valid = false;
      }

      if (!email.value.trim() || !isValidEmail(email.value)) {
        showError('email', 'Informe um e-mail válido.');
        valid = false;
      }

      if (!message.value.trim()) {
        showError('message', 'Escreva uma mensagem.');
        valid = false;
      }

      if (valid) {
        successMsg.hidden = false;
        contactForm.reset();
        setTimeout(() => { successMsg.hidden = true; }, 5000);
      }
    });
  }

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function showError(field, msg) {
    const input = document.getElementById(field);
    const error = document.getElementById(`${field}-error`);
    input.classList.add('error');
    error.textContent = msg;
  }

  function clearErrors() {
    contactForm.querySelectorAll('.form-error').forEach((el) => {
      el.textContent = '';
    });
    contactForm.querySelectorAll('.error').forEach((el) => {
      el.classList.remove('error');
    });
  }

  /* Prevent placeholder project links from navigating */
  document.querySelectorAll('.project-card__link[href="#"]').forEach((link) => {
    link.addEventListener('click', (e) => e.preventDefault());
  });

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
