# Contributing to Cattle Disease AI

Thank you for your interest in contributing to Cattle Disease AI! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear descriptive title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Device/OS information
   - App version

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear feature description
   - Use cases
   - Why it would be beneficial
   - Possible implementation approach

### Code Contributions

#### 1. Fork and Clone

```bash
fork https://github.com/nmaketh/Cattle_disease-ai
git clone https://github.com/YOUR_USERNAME/Cattle_disease-ai
cd Cattle_disease-ai
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

#### 3. Make Changes

- Follow the existing code style
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

#### 4. Test Your Changes

```bash
flutter analyze
flutter test
flutter run
```

#### 5. Commit

```bash
git add .
git commit -m "feat: add new feature description"
# or
git commit -m "fix: fix bug description"
```

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots for UI changes
- Test results

## Code Style Guidelines

### Dart Style

Follow [Effective Dart](https://dart.dev/guides/language/effective-dart):

```dart
// Good
class DiagnosisCase {
  final String diseaseName;
  
  const DiagnosisCase({required this.diseaseName});
}

// Use meaningful names
Future<void> saveDiagnosis() async { }

// Prefer const constructors
const SizedBox(height: 16)
```

### File Organization

```
lib/
├── models/         # Data models only
├── services/       # Business logic
├── screens/        # Full-page screens
├── widgets/        # Reusable components
└── utils/          # Helper functions
```

### Comments

- Write self-documenting code
- Add comments for complex logic
- Use doc comments for public APIs

```dart
/// Runs inference on the provided image.
///
/// Returns a [DiseasePrediction] with the diagnosis results.
/// Throws an exception if inference fails.
Future<DiseasePrediction> predict(String imagePath) async { }
```

## Testing Guidelines

### Write Tests

- Unit tests for business logic
- Widget tests for UI components
- Integration tests for flows

```dart
test('should save diagnosis to database', () async {
  final diagnosis = DiagnosisCase(...);
  final saved = await dbService.insertDiagnosis(diagnosis);
  expect(saved.id, isNotNull);
});
```

### Run Tests

```bash
flutter test                    # All tests
flutter test test/widget_test.dart  # Specific file
```

## Documentation

### Update Documentation

When making changes, update:
- README.md - If it affects usage
- ARCHITECTURE.md - For structural changes
- USER_GUIDE.md - For user-facing features
- Code comments - For implementation details

### Write Clear Docs

- Use simple language
- Include examples
- Add screenshots for UI
- Keep it up to date

## Pull Request Process

1. **Ensure CI passes**
   - All tests pass
   - Code analysis passes
   - No merge conflicts

2. **Get reviewed**
   - At least one approval required
   - Address review comments
   - Update as needed

3. **Squash commits** (if needed)
   - Keep history clean
   - One logical change per commit

4. **Merge**
   - Will be merged by maintainers
   - PR will be closed
   - Branch can be deleted

## Areas Needing Help

We especially welcome contributions in:

- 🤖 **ML Models**: Better disease detection models
- 🧪 **Testing**: More comprehensive tests
- 🌍 **Localization**: Multi-language support
- 📱 **UI/UX**: Interface improvements
- 📝 **Documentation**: Guides and tutorials
- 🐛 **Bug Fixes**: Any bug reports
- ⚡ **Performance**: Optimizations

## Community Guidelines

### Be Respectful

- Use welcoming language
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the project

### Be Collaborative

- Help others learn
- Share knowledge
- Give credit where due
- Work together

### Be Professional

- Keep discussions on-topic
- No spam or self-promotion
- No harassment or discrimination
- Follow code of conduct

## Getting Help

Need help contributing?

- 💬 Open a discussion
- 📧 Contact maintainers
- 📖 Read the documentation
- 🔍 Search existing issues

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the app (major contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask questions by:
- Opening an issue
- Starting a discussion
- Contacting maintainers

Thank you for contributing to Cattle Disease AI! 🐄🤖
