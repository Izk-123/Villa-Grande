/**
 * Villa Grande Lodge - Modern Booking Form JavaScript
 * Enhanced animations and interactions
 */

(function() {
    'use strict';

    class BookingFormManager {
        constructor() {
            this.form = document.querySelector('.modern-booking-form');
            if (!this.form) return;
            
            this.initFloatingLabels();
            this.initDatePickers();
            this.initPriceCalculator();
            this.initRoomSelection();
            this.initStepNavigation();
            this.initFormValidation();
            this.initAutoSave();
            this.initInputMasks();
        }

        // Floating Labels Animation
        initFloatingLabels() {
            const inputs = document.querySelectorAll('.floating-label-group input, .floating-label-group select, .floating-label-group textarea');
            
            inputs.forEach(input => {
                // Check initial value
                if (input.value) {
                    input.closest('.floating-label-group').classList.add('has-value');
                }

                // Focus events
                input.addEventListener('focus', () => {
                    input.closest('.floating-label-group').classList.add('focused');
                });

                input.addEventListener('blur', () => {
                    input.closest('.floating-label-group').classList.remove('focused');
                    if (input.value) {
                        input.closest('.floating-label-group').classList.add('has-value');
                    } else {
                        input.closest('.floating-label-group').classList.remove('has-value');
                    }
                });

                // Animate on input
                input.addEventListener('input', () => {
                    if (input.value) {
                        input.closest('.floating-label-group').classList.add('has-value');
                    } else {
                        input.closest('.floating-label-group').classList.remove('has-value');
                    }
                });
            });
        }

        // Smart Date Picker with Animations
        initDatePickers() {
            const checkIn = document.getElementById('check_in');
            const checkOut = document.getElementById('check_out');
            
            if (!checkIn || !checkOut) return;

            // Set min dates
            const today = new Date().toISOString().split('T')[0];
            checkIn.min = today;
            
            // Update checkout min when checkin changes
            checkIn.addEventListener('change', () => {
                const checkInDate = new Date(checkIn.value);
                const nextDay = new Date(checkInDate);
                nextDay.setDate(checkInDate.getDate() + 1);
                
                checkOut.min = nextDay.toISOString().split('T')[0];
                
                // If current checkout is before new min, update it
                if (new Date(checkOut.value) <= checkInDate) {
                    checkOut.value = nextDay.toISOString().split('T')[0];
                }
                
                // Trigger price calculation
                this.calculatePrice();
                
                // Animate date change
                this.animateDateChange(checkIn);
            });
            
            checkOut.addEventListener('change', () => {
                this.calculatePrice();
                this.animateDateChange(checkOut);
            });
        }

        // Animate date field on change
        animateDateChange(element) {
            element.style.transform = 'scale(1.02)';
            element.style.transition = 'transform 0.2s ease';
            
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 200);
        }

        // Dynamic Price Calculator
        initPriceCalculator() {
            this.priceCalculator = document.createElement('div');
            this.priceCalculator.className = 'price-calculator';
            this.priceCalculator.style.display = 'none';
            
            const roomSelect = document.getElementById('room_select');
            if (roomSelect) {
                roomSelect.addEventListener('change', () => this.calculatePrice());
            }
        }

        calculatePrice() {
            const checkIn = document.getElementById('check_in');
            const checkOut = document.getElementById('check_out');
            const roomSelect = document.getElementById('room_select');
            
            if (!checkIn?.value || !checkOut?.value || !roomSelect?.value) {
                this.priceCalculator.style.display = 'none';
                return;
            }
            
            const nights = this.calculateNights(checkIn.value, checkOut.value);
            if (nights <= 0) return;
            
            // Get room price from selected option data attribute
            const selectedOption = roomSelect.options[roomSelect.selectedIndex];
            const pricePerNight = parseFloat(selectedOption.dataset.price || 0);
            
            if (pricePerNight <= 0) return;
            
            const subtotal = pricePerNight * nights;
            const tax = subtotal * 0.1; // 10% tax
            const total = subtotal + tax;
            
            this.updatePriceDisplay(nights, pricePerNight, subtotal, tax, total);
        }

        calculateNights(checkIn, checkOut) {
            const start = new Date(checkIn);
            const end = new Date(checkOut);
            const diffTime = Math.abs(end - start);
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        }

        updatePriceDisplay(nights, pricePerNight, subtotal, tax, total) {
            this.priceCalculator.innerHTML = `
                <div class="price-row">
                    <span class="price-label">Nights:</span>
                    <span class="price-value">${nights}</span>
                </div>
                <div class="price-row">
                    <span class="price-label">Rate per night:</span>
                    <span class="price-value">$${pricePerNight.toFixed(2)}</span>
                </div>
                <div class="price-row">
                    <span class="price-label">Subtotal:</span>
                    <span class="price-value">$${subtotal.toFixed(2)}</span>
                </div>
                <div class="price-row">
                    <span class="price-label">Tax (10%):</span>
                    <span class="price-value">$${tax.toFixed(2)}</span>
                </div>
                <div class="price-row total">
                    <span class="price-label">Total:</span>
                    <span class="price-value">$${total.toFixed(2)}</span>
                </div>
            `;
            
            this.priceCalculator.style.display = 'block';
            
            // Animate the calculator
            this.priceCalculator.style.animation = 'none';
            this.priceCalculator.offsetHeight; // Trigger reflow
            this.priceCalculator.style.animation = 'pricePulse 2s infinite';
            
            // Insert after room selection
            const roomSection = document.querySelector('.form-section:nth-child(3)');
            if (roomSection && !roomSection.contains(this.priceCalculator)) {
                roomSection.appendChild(this.priceCalculator);
            }
        }

        // Enhanced Room Selection
        initRoomSelection() {
            const roomSelect = document.getElementById('room_select');
            if (!roomSelect) return;
            
            // Transform select into card-style selection
            this.transformRoomSelection(roomSelect);
        }

        transformRoomSelection(select) {
            const container = document.createElement('div');
            container.className = 'room-selection-container';
            container.style.cssText = 'max-height: 300px; overflow-y: auto; padding-right: 10px;';
            
            // Get all options
            Array.from(select.options).forEach((option, index) => {
                if (index === 0) return; // Skip placeholder
                
                const roomCard = this.createRoomCard(option, select.value === option.value);
                container.appendChild(roomCard);
            });
            
            // Replace select with cards
            select.style.display = 'none';
            select.parentNode.insertBefore(container, select.nextSibling);
            
            // Store reference
            this.roomCards = container;
        }

        createRoomCard(option, isSelected) {
            const card = document.createElement('div');
            card.className = `room-card-option ${isSelected ? 'selected' : ''}`;
            card.dataset.value = option.value;
            
            // Get room details from data attributes
            const roomType = option.text.split(' - ')[0];
            const roomNumber = option.text.split(' - ')[1] || '';
            const price = option.dataset.price || '0';
            
            card.innerHTML = `
                <div class="room-type-badge">${roomType}</div>
                <h4 style="font-size: 1.1rem; margin-bottom: 5px;">${roomNumber}</h4>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: var(--gold); font-weight: 600;">$${price}/night</span>
                    <span style="font-size: 0.8rem; color: rgba(10,35,66,0.5);">${option.dataset.capacity || '2'} guests</span>
                </div>
            `;
            
            card.addEventListener('click', () => {
                // Remove selection from all cards
                document.querySelectorAll('.room-card-option').forEach(c => {
                    c.classList.remove('selected');
                });
                
                // Select this card
                card.classList.add('selected');
                
                // Update original select
                const select = document.getElementById('room_select');
                select.value = option.value;
                
                // Trigger change event
                select.dispatchEvent(new Event('change', { bubbles: true }));
                
                // Animate selection
                this.animateRoomSelection(card);
            });
            
            return card;
        }

        animateRoomSelection(card) {
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
            }, 150);
        }

        // Step Navigation with Animations
        initStepNavigation() {
            this.currentStep = 0;
            this.steps = document.querySelectorAll('.form-section');
            this.stepIndicators = document.querySelectorAll('.step-item');
            
            if (!this.steps.length) return;
            
            this.showStep(this.currentStep);
            
            // Add navigation buttons
            this.addNavigationButtons();
        }

        showStep(stepIndex) {
            this.steps.forEach((step, index) => {
                if (index === stepIndex) {
                    step.style.display = 'block';
                    step.style.animation = 'sectionSlide 0.5s ease-out';
                } else {
                    step.style.display = 'none';
                }
            });
            
            this.stepIndicators.forEach((indicator, index) => {
                if (index < stepIndex) {
                    indicator.classList.add('completed');
                    indicator.classList.remove('active');
                } else if (index === stepIndex) {
                    indicator.classList.add('active');
                    indicator.classList.remove('completed');
                } else {
                    indicator.classList.remove('active', 'completed');
                }
            });
            
            this.currentStep = stepIndex;
        }

        addNavigationButtons() {
            const navContainer = document.createElement('div');
            navContainer.className = 'step-navigation';
            navContainer.style.cssText = 'display: flex; justify-content: space-between; margin-top: 30px;';
            
            const prevBtn = document.createElement('button');
            prevBtn.type = 'button';
            prevBtn.className = 'btn-vg-outline';
            prevBtn.innerHTML = '<i class="fas fa-arrow-left"></i> Previous';
            prevBtn.style.display = this.currentStep === 0 ? 'none' : 'flex';
            
            const nextBtn = document.createElement('button');
            nextBtn.type = 'button';
            nextBtn.className = 'btn-vg-primary';
            nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
            nextBtn.style.display = this.currentStep === this.steps.length - 1 ? 'none' : 'flex';
            
            const submitBtn = document.createElement('button');
            submitBtn.type = 'submit';
            submitBtn.className = 'modern-submit-btn';
            submitBtn.innerHTML = '<span class="btn-text">Complete Booking</span>';
            submitBtn.style.display = this.currentStep === this.steps.length - 1 ? 'flex' : 'none';
            
            prevBtn.addEventListener('click', () => {
                if (this.currentStep > 0) {
                    this.showStep(this.currentStep - 1);
                }
            });
            
            nextBtn.addEventListener('click', () => {
                if (this.validateStep(this.currentStep)) {
                    if (this.currentStep < this.steps.length - 1) {
                        this.showStep(this.currentStep + 1);
                    }
                }
            });
            
            navContainer.appendChild(prevBtn);
            navContainer.appendChild(nextBtn);
            navContainer.appendChild(submitBtn);
            
            this.form.appendChild(navContainer);
            
            // Update navigation on step change
            const originalShowStep = this.showStep.bind(this);
            this.showStep = (stepIndex) => {
                originalShowStep(stepIndex);
                
                prevBtn.style.display = stepIndex === 0 ? 'none' : 'flex';
                nextBtn.style.display = stepIndex === this.steps.length - 1 ? 'none' : 'flex';
                submitBtn.style.display = stepIndex === this.steps.length - 1 ? 'flex' : 'none';
            };
        }

        validateStep(stepIndex) {
            const step = this.steps[stepIndex];
            const inputs = step.querySelectorAll('input, select, textarea');
            let isValid = true;
            
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value) {
                    this.showError(input, 'This field is required');
                    isValid = false;
                }
            });
            
            return isValid;
        }

        // Form Validation with Animations
        initFormValidation() {
            this.form.addEventListener('submit', (e) => {
                if (!this.validateForm()) {
                    e.preventDefault();
                } else {
                    this.showLoadingState(e.target.querySelector('button[type="submit"]'));
                }
            });
        }

        validateForm() {
            let isValid = true;
            const requiredFields = this.form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value) {
                    this.showError(field, 'This field is required');
                    isValid = false;
                } else {
                    this.clearError(field);
                }
            });
            
            // Email validation
            const email = this.form.querySelector('input[type="email"]');
            if (email && email.value && !this.isValidEmail(email.value)) {
                this.showError(email, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Phone validation
            const phone = this.form.querySelector('input[name="phone"]');
            if (phone && phone.value && !this.isValidPhone(phone.value)) {
                this.showError(phone, 'Please enter a valid phone number');
                isValid = false;
            }
            
            return isValid;
        }

        showError(field, message) {
            field.classList.add('error');
            
            // Remove existing error message
            const existingError = field.parentNode.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            
            // Add new error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            
            field.parentNode.appendChild(errorDiv);
            
            // Shake animation
            field.style.animation = 'shake 0.5s ease';
            setTimeout(() => {
                field.style.animation = '';
            }, 500);
        }

        clearError(field) {
            field.classList.remove('error');
            const errorMessage = field.parentNode.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        }

        isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }

        isValidPhone(phone) {
            const cleaned = phone.replace(/[\s\-\(\)\+]/g, '');
            return cleaned.length >= 9 && /^\d+$/.test(cleaned);
        }

        showLoadingState(button) {
            const originalText = button.innerHTML;
            button.innerHTML = '<span class="btn-spinner"></span> Processing...';
            button.disabled = true;
            
            // Simulate processing (remove in production)
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        }

        // Auto-save Form Data
        initAutoSave() {
            const inputs = this.form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                input.addEventListener('change', () => {
                    this.saveFormData();
                });
                
                input.addEventListener('keyup', this.debounce(() => {
                    this.saveFormData();
                }, 1000));
            });
            
            // Load saved data
            this.loadFormData();
        }

        saveFormData() {
            const formData = new FormData(this.form);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            localStorage.setItem('bookingFormData', JSON.stringify(data));
            
            // Show saved indicator
            this.showSavedIndicator();
        }

        loadFormData() {
            const saved = localStorage.getItem('bookingFormData');
            if (!saved) return;
            
            try {
                const data = JSON.parse(saved);
                
                Object.keys(data).forEach(key => {
                    const field = this.form.querySelector(`[name="${key}"]`);
                    if (field) {
                        field.value = data[key];
                        // Trigger change event
                        field.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                });
            } catch (e) {
                console.error('Error loading saved form data:', e);
            }
        }

        showSavedIndicator() {
            let indicator = document.querySelector('.auto-save-indicator');
            
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.className = 'auto-save-indicator';
                indicator.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: var(--navy);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 30px;
                    font-size: 0.8rem;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                    z-index: 9999;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                indicator.innerHTML = '<i class="fas fa-check-circle" style="color: var(--gold);"></i> Draft saved';
                document.body.appendChild(indicator);
            }
            
            indicator.style.opacity = '1';
            
            clearTimeout(this.saveTimeout);
            this.saveTimeout = setTimeout(() => {
                indicator.style.opacity = '0';
            }, 2000);
        }

        // Input Masks
        initInputMasks() {
            const phoneInput = this.form.querySelector('input[name="phone"]');
            if (phoneInput) {
                phoneInput.addEventListener('input', (e) => {
                    let value = e.target.value.replace(/\D/g, '');
                    if (value.length > 0) {
                        if (value.length <= 3) {
                            value = value;
                        } else if (value.length <= 6) {
                            value = value.slice(0,3) + ' ' + value.slice(3);
                        } else {
                            value = value.slice(0,3) + ' ' + value.slice(3,6) + ' ' + value.slice(6,9);
                        }
                    }
                    e.target.value = value;
                });
            }
        }

        // Utility: Debounce
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    }

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        new BookingFormManager();
    });

})();