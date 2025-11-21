# 🤝 Contributing to VEra-Resonance

First off, thank you for considering contributing to **VEra-Resonance**! It's people like you that make this project a reality.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Community](#community)

---

## 📜 Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

**TL;DR:**
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

---

## 🚀 Getting Started

### Prerequisites

```bash
- Python 3.9+
- Git
- MetaMask or compatible wallet
- Basic understanding of Web3
```

### Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork:
git clone https://github.com/YOUR_USERNAME/AEra-LogIn.git
cd AEra-LogIn

# Add upstream remote
git remote add upstream https://github.com/VEra-Resonance/AEra-LogIn.git
```

---

## 💡 How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check existing [Issues](https://github.com/VEra-Resonance/AEra-LogIn/issues)
- Test with the latest version
- Collect relevant information (logs, screenshots, environment)

**When submitting:**
```markdown
**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10
- Browser: Chrome 120

**Steps to Reproduce:**
1. Start server
2. Connect wallet
3. Click verify
4. Error appears

**Expected Behavior:**
Signature should be verified

**Actual Behavior:**
Error: "Invalid signature"

**Logs:**
[Paste relevant logs]
```

### ✨ Suggesting Features

**Before suggesting:**
- Check [existing feature requests](https://github.com/VEra-Resonance/AEra-LogIn/issues?q=label%3Aenhancement)
- Make sure it aligns with project goals

**When suggesting:**
```markdown
**Problem:**
Current login flow is slow on mobile

**Solution:**
Add QR code login for mobile wallets

**Benefits:**
- Faster mobile UX
- Better conversion rate
- Cross-device support

**Implementation Ideas:**
- WalletConnect integration
- QR code generation library
- Mobile-first UI
```

### 📝 Improving Documentation

Documentation is crucial! You can help by:
- Fixing typos
- Clarifying confusing sections
- Adding examples
- Translating to other languages

---

## 🛠️ Development Setup

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### 2. Environment Configuration

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

### 3. Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_api.py

# With coverage
pytest --cov=src tests/
```

### 4. Start Development Server

```bash
# Run locally
python3 server.py

# Server runs on http://localhost:8820
```

---

## 🔄 Pull Request Process

### 1. Create Feature Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/amazing-feature
```

### 2. Make Changes

```bash
# Write code
# Add tests
# Update documentation

# Check code style
black . --check
flake8 .

# Run tests
pytest
```

### 3. Commit Changes

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): description

git commit -m "feat(auth): add QR code login support

- Integrate WalletConnect
- Add QR generation
- Update UI for mobile
- Add tests

Closes #42"
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### 4. Push & Create PR

```bash
# Push to your fork
git push origin feature/amazing-feature

# Go to GitHub and create Pull Request
```

**PR Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings

## Screenshots (if applicable)
[Add screenshots]
```

### 5. Review Process

- Maintainers will review your PR
- Address feedback in new commits
- Keep PR focused (one feature per PR)
- Be patient and respectful

### 6. Merge

Once approved:
- Maintainers will merge
- Your contribution will be in the next release!
- You'll be added to [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 📐 Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/):

```python
# Good
def calculate_resonance_score(wallet_address: str, login_count: int) -> int:
    """
    Calculate resonance score based on wallet activity.
    
    Args:
        wallet_address: Ethereum wallet address
        login_count: Number of logins
        
    Returns:
        Resonance score (0-100)
    """
    base_score = 50
    increment = min(login_count, 50)
    return base_score + increment

# Bad
def calc_score(addr, cnt):
    return 50 + cnt
```

### JavaScript Style

Use ES6+ with modern syntax:

```javascript
// Good
const connectWallet = async () => {
    try {
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        return accounts[0];
    } catch (error) {
        console.error('Wallet connection failed:', error);
        throw error;
    }
};

// Bad
function connectWallet() {
    var accounts = window.ethereum.request({ method: 'eth_requestAccounts' });
    return accounts[0];
}
```

### Documentation

```python
# Always add docstrings
def verify_signature(address: str, message: str, signature: str) -> bool:
    """
    Verify EIP-191 signature.
    
    Args:
        address: Ethereum address (0x...)
        message: Message that was signed
        signature: Signature hex string (0x...)
        
    Returns:
        True if signature is valid, False otherwise
        
    Raises:
        ValueError: If address format is invalid
        
    Example:
        >>> verify_signature("0xabc...", "Login to VEra-Resonance", "0x123...")
        True
    """
```

### Testing

```python
# Write comprehensive tests
def test_resonance_score_calculation():
    """Test that resonance score increases with logins."""
    # Arrange
    wallet = "0xtest"
    initial_score = calculate_score(wallet, 0)
    
    # Act
    score_after_10_logins = calculate_score(wallet, 10)
    
    # Assert
    assert score_after_10_logins > initial_score
    assert score_after_10_logins <= 100
```

---

## 🎨 Project Structure

```
src/
├── api/              # API endpoints
│   ├── auth.py
│   ├── user.py
│   └── stats.py
├── db/               # Database layer
│   ├── models.py
│   └── queries.py
├── scoring/          # Scoring logic
│   ├── calculator.py
│   └── patterns.py
└── utils/            # Utilities
    ├── crypto.py
    └── validators.py
```

**Guidelines:**
- One file per logical component
- Max 300 lines per file
- Clear naming conventions
- Avoid circular imports

---

## 🧪 Testing Guidelines

### Unit Tests

```python
# tests/test_scoring.py
def test_score_increment():
    """Score should increase by 1 per login up to 50."""
    assert calculate_score(0) == 50
    assert calculate_score(1) == 51
    assert calculate_score(50) == 100
    assert calculate_score(100) == 100  # Capped at 100
```

### Integration Tests

```python
# tests/test_api.py
def test_verify_endpoint(client):
    """Test complete verification flow."""
    # Get nonce
    response = client.post("/api/nonce", json={"address": TEST_ADDRESS})
    nonce = response.json()["nonce"]
    
    # Sign message
    signature = sign_message(TEST_PRIVATE_KEY, nonce)
    
    # Verify
    response = client.post("/api/verify", json={
        "address": TEST_ADDRESS,
        "signature": signature,
        "nonce": nonce
    })
    
    assert response.status_code == 200
    assert response.json()["is_human"] == True
```

### Test Coverage

- Aim for **80%+ coverage**
- Cover edge cases
- Test error handling
- Mock external dependencies

---

## 📦 Release Process

**For Maintainers:**

```bash
# 1. Update version
# Edit version in server.py and package.json

# 2. Update CHANGELOG.md
# Add release notes

# 3. Create tag
git tag -a v0.2.0 -m "Release v0.2.0 - QR Code Login"
git push origin v0.2.0

# 4. Create GitHub Release
# Go to Releases → Draft new release
# Add changelog and binaries

# 5. Announce
# Twitter, Discord, Telegram
```

---

## 🌍 Community

### Communication Channels

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - Questions, ideas
- **Discord** - [discord.gg/vera](https://discord.gg/vera)
- **Telegram** - [t.me/VeraResonance](https://t.me/VeraResonance)
- **Twitter/X** - [@VeraResonanz](https://twitter.com/VeraResonanz)

### Getting Help

**Before asking:**
- Read documentation
- Search existing issues
- Check FAQ

**When asking:**
- Be specific
- Provide context
- Show what you've tried
- Share relevant code/logs

---

## 🏆 Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- Project website
- Social media shoutouts

**Types of contributions:**
- 💻 Code
- 📝 Documentation
- 🐛 Bug reports
- 💡 Ideas
- 🌍 Translations
- 🎨 Design
- 📢 Community support

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the **Apache License 2.0** license.

See [LICENSE](LICENSE) for details.

---

## ❓ Questions?

Don't hesitate to reach out:
- Open a [Discussion](https://github.com/VEra-Resonance/AEra-LogIn/discussions)
- Join our [Discord](https://discord.gg/vera)
- Email: contributors@vera-resonance.org

---

**Thank you for contributing to VEra-Resonance!** 🎉

Every contribution, no matter how small, helps build a better future for decentralized proof-of-humanity.

---

*This document is adapted from the [Contributor Covenant](https://www.contributor-covenant.org/) and various open-source project guidelines.*

---

**VEra-Resonance © 2025 Karlheinz Beismann** ⸻ Apache License 2.0
