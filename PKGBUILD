# Maintainer: Your Name <your.email@example.com>
pkgname=quizr
pkgver=1.0.0
pkgrel=1
pkgdesc="A command-line quiz tool with spaced repetition"
arch=('any')
url="https://github.com/yourusername/quizr"
license=('CC0')
depends=('python' 'python-yaml' 'python-click' 'python-fuzzywuzzy' 'python-levenshtein')
makedepends=('python-build' 'python-installer' 'python-wheel')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Replace with actual hash after first release

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
} 