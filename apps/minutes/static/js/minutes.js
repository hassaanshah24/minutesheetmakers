document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    if (!form || !$('.select2').length) return;

    // Initialize Select2
    $('.select2').select2({
        placeholder: "Select Approvers",
        allowClear: true,
    });

    // Validate form submission for empty approval chain
    form.addEventListener('submit', function (e) {
        const approvalChain = $('.select2').val();
        if (!approvalChain || approvalChain.length === 0) {
            e.preventDefault();
            alert("Approval Chain cannot be empty!");
        }
    });
});
