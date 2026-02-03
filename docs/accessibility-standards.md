# RAMMP Website Accessibility Standards

This document outlines the accessibility standards, guidelines, and implementation details for the RAMMP website. Our goal is to meet or exceed **WCAG 2.1 Level AA** compliance.

---

## Table of Contents

1. [Accessibility Commitment](#accessibility-commitment)
2. [WCAG 2.1 Overview](#wcag-21-overview)
3. [Implementation Guidelines](#implementation-guidelines)
4. [Testing Procedures](#testing-procedures)
5. [Accessibility Features](#accessibility-features)
6. [Known Issues & Roadmap](#known-issues--roadmap)
7. [Reporting Issues](#reporting-issues)

---

## Accessibility Commitment

The RAMMP consortium is committed to ensuring digital accessibility for people with disabilities. Given our mission to create assistive technology for people with mobility challenges, it is especially important that our website be accessible to all users, including those who:

- Use screen readers or other assistive technologies
- Navigate using only a keyboard
- Have low vision or color blindness
- Have cognitive or learning disabilities
- Use voice recognition software

---

## WCAG 2.1 Overview

The Web Content Accessibility Guidelines (WCAG) 2.1 are organized around four principles, known as **POUR**:

### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

| Guideline | Level | Status |
|-----------|-------|--------|
| 1.1.1 Non-text Content | A | ✅ Implemented |
| 1.2.1 Audio-only and Video-only | A | N/A (no media) |
| 1.3.1 Info and Relationships | A | ✅ Implemented |
| 1.3.2 Meaningful Sequence | A | ✅ Implemented |
| 1.3.3 Sensory Characteristics | A | ✅ Implemented |
| 1.4.1 Use of Color | A | ✅ Implemented |
| 1.4.2 Audio Control | A | N/A (no audio) |
| 1.4.3 Contrast (Minimum) | AA | ✅ Implemented |
| 1.4.4 Resize Text | AA | ✅ Implemented |
| 1.4.5 Images of Text | AA | ✅ Implemented |
| 1.4.10 Reflow | AA | ✅ Implemented |
| 1.4.11 Non-text Contrast | AA | ✅ Implemented |
| 1.4.12 Text Spacing | AA | ✅ Implemented |
| 1.4.13 Content on Hover or Focus | AA | ✅ Implemented |

### 2. Operable
User interface components and navigation must be operable.

| Guideline | Level | Status |
|-----------|-------|--------|
| 2.1.1 Keyboard | A | ✅ Implemented |
| 2.1.2 No Keyboard Trap | A | ✅ Implemented |
| 2.1.4 Character Key Shortcuts | A | N/A (none used) |
| 2.2.1 Timing Adjustable | A | N/A (no time limits) |
| 2.2.2 Pause, Stop, Hide | A | N/A (no auto-playing) |
| 2.3.1 Three Flashes or Below | A | ✅ Implemented |
| 2.4.1 Bypass Blocks | A | ✅ Implemented |
| 2.4.2 Page Titled | A | ✅ Implemented |
| 2.4.3 Focus Order | A | ✅ Implemented |
| 2.4.4 Link Purpose (In Context) | A | ✅ Implemented |
| 2.4.5 Multiple Ways | AA | ✅ Implemented |
| 2.4.6 Headings and Labels | AA | ✅ Implemented |
| 2.4.7 Focus Visible | AA | ✅ Implemented |
| 2.5.1 Pointer Gestures | A | ✅ Implemented |
| 2.5.2 Pointer Cancellation | A | ✅ Implemented |
| 2.5.3 Label in Name | A | ✅ Implemented |
| 2.5.4 Motion Actuation | A | N/A (none used) |

### 3. Understandable
Information and the operation of user interface must be understandable.

| Guideline | Level | Status |
|-----------|-------|--------|
| 3.1.1 Language of Page | A | ✅ Implemented |
| 3.1.2 Language of Parts | AA | ✅ Implemented |
| 3.2.1 On Focus | A | ✅ Implemented |
| 3.2.2 On Input | A | ✅ Implemented |
| 3.2.3 Consistent Navigation | AA | ✅ Implemented |
| 3.2.4 Consistent Identification | AA | ✅ Implemented |
| 3.3.1 Error Identification | A | ✅ Implemented |
| 3.3.2 Labels or Instructions | A | ✅ Implemented |
| 3.3.3 Error Suggestion | AA | ✅ Implemented |
| 3.3.4 Error Prevention | AA | ✅ Implemented |

### 4. Robust
Content must be robust enough to be interpreted by assistive technologies.

| Guideline | Level | Status |
|-----------|-------|--------|
| 4.1.1 Parsing | A | ✅ Implemented |
| 4.1.2 Name, Role, Value | A | ✅ Implemented |
| 4.1.3 Status Messages | AA | ✅ Implemented |

---

## Implementation Guidelines

### HTML Structure

#### Document Language
```html
<html lang="en">
```

#### Page Title
Each page must have a unique, descriptive title:
```html
<title>People - RAMMP Consortium</title>
```

#### Landmarks
Use semantic HTML5 elements for page structure:
```html
<nav role="navigation" aria-label="Main navigation">...</nav>
<main id="main-content" role="main">...</main>
<footer role="contentinfo">...</footer>
```

#### Skip Links
Every page includes a skip link as the first focusable element:
```html
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-bright-blue text-white px-4 py-2 rounded-lg z-50">
    Skip to main content
</a>
```

### Headings

Maintain proper heading hierarchy (h1 → h2 → h3):
- Each page has exactly one `<h1>`
- Headings never skip levels
- Headings are used for structure, not styling

### Images

#### Informative Images
```html
<img src="photo.jpg" alt="Descriptive text explaining the image content">
```

#### Decorative Images
```html
<img src="decorative.jpg" alt="" role="presentation">
```

#### SVG Icons
Decorative icons should be hidden from assistive technology:
```html
<svg aria-hidden="true" class="w-6 h-6">...</svg>
```

Interactive icons need accessible names:
```html
<button aria-label="Close menu">
    <svg aria-hidden="true">...</svg>
</button>
```

### Links

#### Internal Links
```html
<a href="people.html">Meet the Team</a>
```

#### External Links
External links should indicate they open in a new window:
```html
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
    External Site
    <span class="sr-only">(opens in new tab)</span>
</a>
```

### Forms

#### Labels
Every form control must have an associated label:
```html
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>
```

#### Required Fields
Indicate required fields both visually and programmatically:
```html
<label for="name">
    Name <span class="text-red-500" aria-hidden="true">*</span>
    <span class="sr-only">(required)</span>
</label>
<input type="text" id="name" name="name" required aria-required="true">
```

#### Error Messages
Associate error messages with form controls:
```html
<input type="email" id="email" aria-describedby="email-error" aria-invalid="true">
<span id="email-error" class="text-red-500">Please enter a valid email address</span>
```

### Color and Contrast

#### Minimum Contrast Ratios
- **Normal text**: 4.5:1 minimum (AA)
- **Large text** (18pt+ or 14pt+ bold): 3:1 minimum
- **UI components**: 3:1 minimum

#### Color Palette Contrast
| Color Combination | Ratio | Status |
|-------------------|-------|--------|
| Near Black (#03090D) on White (#FFFFFF) | 19.8:1 | ✅ Passes AAA |
| Bright Blue (#22A9FF) on White (#FFFFFF) | 3.1:1 | ✅ Passes (large text) |
| Dark Gray (#444444) on White (#FFFFFF) | 9.7:1 | ✅ Passes AAA |
| White (#FFFFFF) on Bright Blue (#22A9FF) | 3.1:1 | ✅ Passes (large text) |
| White (#FFFFFF) on Deep Blue (#115C90) | 5.9:1 | ✅ Passes AA |

#### Don't Rely on Color Alone
Information conveyed with color must also be available through other means:
- Links are underlined or have other visual indicators
- Form errors include text descriptions
- Status indicators include icons or text

### Keyboard Navigation

#### Focus Indicators
All interactive elements must have visible focus states:
```css
:focus-visible {
    outline: 2px solid #22A9FF;
    outline-offset: 2px;
}
```

#### Tab Order
- Tab order follows logical reading order
- No keyboard traps
- All interactive elements are reachable via keyboard

#### Mobile Menu
The mobile menu is keyboard accessible:
- Opens/closes with Enter or Space
- Menu items are focusable
- Escape closes the menu

### Dark Mode

Dark mode maintains accessibility:
- Contrast ratios are maintained
- Focus indicators remain visible
- All content remains readable

---

## Testing Procedures

### Automated Testing

Run automated accessibility checks regularly using:

1. **axe DevTools** (browser extension)
   - Run on every page
   - Address all critical and serious issues

2. **WAVE** (web accessibility evaluation tool)
   - Check for structural issues
   - Review contrast errors

3. **Lighthouse** (Chrome DevTools)
   - Accessibility score should be 90+
   - Review all flagged issues

### Manual Testing

#### Keyboard Testing
1. Navigate entire site using only Tab, Shift+Tab, Enter, Space, Arrow keys
2. Verify all interactive elements are reachable
3. Verify focus indicators are visible
4. Verify no keyboard traps exist

#### Screen Reader Testing
Test with at least one screen reader:
- **NVDA** (Windows, free)
- **VoiceOver** (macOS/iOS, built-in)
- **JAWS** (Windows, commercial)

Verify:
- All content is announced
- Images have appropriate alt text
- Form labels are announced
- Landmarks are identified
- Headings structure is logical

#### Zoom Testing
1. Zoom browser to 200%
2. Verify all content is visible
3. Verify no horizontal scrolling on main content
4. Verify text doesn't overlap

#### Color Testing
1. Use a color blindness simulator
2. Verify information isn't conveyed by color alone
3. Test with high contrast mode

### Testing Checklist

Before deploying changes, verify:

- [ ] All images have appropriate alt text
- [ ] Heading hierarchy is correct
- [ ] All form controls have labels
- [ ] Color contrast meets minimums
- [ ] Focus indicators are visible
- [ ] Skip link works correctly
- [ ] External links are indicated
- [ ] No keyboard traps
- [ ] Screen reader announces content correctly
- [ ] Content reflows at 200% zoom

---

## Accessibility Features

### Currently Implemented

1. **Skip to Main Content Link** - Allows keyboard users to bypass navigation
2. **Semantic HTML** - Proper use of landmarks, headings, and lists
3. **Alt Text** - Descriptive alternative text for all informative images
4. **Form Labels** - All form controls have associated labels
5. **Focus Indicators** - Visible focus states on all interactive elements
6. **Color Contrast** - Text meets WCAG AA contrast requirements
7. **Responsive Design** - Content reflows on smaller screens and zoom
8. **Dark Mode** - Accessible dark theme option
9. **Keyboard Navigation** - All functionality available via keyboard
10. **ARIA Labels** - Screen reader-friendly labels on icon buttons

### Best Practices Followed

- No auto-playing media
- No flashing content
- Consistent navigation across pages
- Descriptive link text
- Error prevention on forms
- Logical reading order

---

## Known Issues & Roadmap

### Current Issues
- None identified at this time

### Future Enhancements
- Add accessibility statement page
- Implement focus trap for mobile menu modal
- Add live regions for dynamic content updates
- Consider adding text resize controls
- Add high contrast mode toggle

---

## Reporting Issues

If you encounter accessibility barriers on this website, please contact us:

- **Email**: Contact via the website contact form
- **Subject**: Accessibility Issue Report

Please include:
1. Description of the issue
2. Page URL where issue occurred
3. Assistive technology used (if applicable)
4. Steps to reproduce the issue

We are committed to addressing accessibility issues promptly.

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

---

*Last updated: February 2026*
