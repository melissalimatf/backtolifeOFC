
  document.querySelectorAll('input[name="clientType"]').forEach(radio => {
    radio.addEventListener('change', function() {
      document.getElementById('rehabFields').classList.toggle('hidden', this.value !== 'rehab');
      document.getElementById('educationFields').classList.toggle('hidden', this.value !== 'education');
    });
  });

  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      document.querySelectorAll('.form-content').forEach(content => content.classList.remove('active'));
      document.getElementById(this.dataset.target).classList.add('active');
    });
  });

