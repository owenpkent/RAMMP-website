# RAMMP Website

Official website for the RAMMP (Robotic Assistive Mobility and Manipulation Platform) consortium.

## About RAMMP

RAMMP is a $41.5 million ARPA-H funded initiative led by the University of Pittsburgh to develop next-generation robotic assistive mobility and manipulation technologies. The consortium brings together leading research institutions to create innovative solutions that empower people with mobility challenges to live independently.

## Consortium Partners

- **University of Pittsburgh** - Human Engineering Research Laboratories (HERL)
- **Carnegie Mellon University** - Robotic Caregiving and Human Interaction Lab
- **Cornell University** - Emprise Lab
- **Northeastern University** - RIVeR Lab
- **Purdue University** - Intelligent Assistive Systems Lab
- **ATDev** - Assistive Technology Development

## Technology Stack

- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first styling
- **JavaScript** - Dark mode toggle and interactions
- **Netlify** - Hosting and form handling

## Development

### Prerequisites

- Node.js (v14 or higher)
- npm

### Installation

```bash
npm install
```

### Build

```bash
npm run build
```

This compiles the Tailwind CSS from `src/input.css` to `dist/output.css`.

### Development Server

```bash
npm run dev
```

Runs Tailwind in watch mode for development.

## Project Structure

```
RAMMP-website/
├── assets/
│   └── images/          # Images and logos
├── dist/
│   └── output.css       # Compiled Tailwind CSS
├── src/
│   └── input.css        # Tailwind source
├── index.html           # Home page
├── people.html          # Team members
├── publications.html    # Research and media coverage
├── progress.html        # Project timeline and updates
├── contact.html         # Contact form
├── package.json         # Dependencies
└── tailwind.config.js   # Tailwind configuration
```

## Contact

For inquiries about the RAMMP project, please visit [rammp.tech/contact](https://rammp.tech/contact) or contact the lead institution at the University of Pittsburgh.

## Funding

This project is funded by the Advanced Research Projects Agency for Health (ARPA-H), U.S. Department of Health and Human Services.

## License

MIT License - see [LICENSE](LICENSE) file for details.
