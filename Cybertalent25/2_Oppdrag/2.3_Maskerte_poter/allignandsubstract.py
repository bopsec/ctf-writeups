import cv2
import numpy as np
import os

def create_output_dir(base_dir="aligned_output"):
    """Create output directory for results"""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

def save_result(img, output_dir, name):
    """Save result image"""
    filepath = os.path.join(output_dir, f"{name}.png")
    if img.dtype == np.float64 or img.dtype == np.float32:
        if img.max() > img.min():
            img = ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)
        else:
            img = np.zeros_like(img, dtype=np.uint8)
    cv2.imwrite(filepath, img)
    print(f"Saved: {name}")

# ============================================
# ALIGNMENT METHODS
# ============================================

def align_feature_matching(watermarked, original):
    """Align using ORB feature matching"""
    print("  Trying ORB feature matching...")
    
    wm_gray = cv2.cvtColor(watermarked, cv2.COLOR_BGR2GRAY)
    orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    orb = cv2.ORB_create(10000)
    kp1, des1 = orb.detectAndCompute(wm_gray, None)
    kp2, des2 = orb.detectAndCompute(orig_gray, None)
    
    if des1 is None or des2 is None:
        return None
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    
    print(f"    Found {len(good_matches)} good matches")
    
    if len(good_matches) < 10:
        return None
    
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    
    if M is None:
        return None
    
    h, w = watermarked.shape[:2]
    aligned = cv2.warpPerspective(original, M, (w, h))
    
    return aligned

def align_sift(watermarked, original):
    """Align using SIFT feature matching"""
    print("  Trying SIFT feature matching...")
    
    try:
        sift = cv2.SIFT_create()
    except:
        print("    SIFT not available")
        return None
    
    wm_gray = cv2.cvtColor(watermarked, cv2.COLOR_BGR2GRAY)
    orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    kp1, des1 = sift.detectAndCompute(wm_gray, None)
    kp2, des2 = sift.detectAndCompute(orig_gray, None)
    
    if des1 is None or des2 is None:
        return None
    
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    
    print(f"    Found {len(good_matches)} good matches")
    
    if len(good_matches) < 10:
        return None
    
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    
    if M is None:
        return None
    
    h, w = watermarked.shape[:2]
    aligned = cv2.warpPerspective(original, M, (w, h))
    
    return aligned

def align_ecc(watermarked, original):
    """Align using ECC (Enhanced Correlation Coefficient)"""
    print("  Trying ECC alignment...")
    
    h, w = watermarked.shape[:2]
    orig_resized = cv2.resize(original, (w, h))
    
    wm_gray = cv2.cvtColor(watermarked, cv2.COLOR_BGR2GRAY).astype(np.float32)
    orig_gray = cv2.cvtColor(orig_resized, cv2.COLOR_BGR2GRAY).astype(np.float32)
    
    warp_mode = cv2.MOTION_AFFINE
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-8)
    
    try:
        cc, warp_matrix = cv2.findTransformECC(wm_gray, orig_gray, warp_matrix, warp_mode, criteria)
        aligned = cv2.warpAffine(orig_resized, warp_matrix, (w, h),
                                  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        print(f"    ECC correlation: {cc:.4f}")
        return aligned
    except Exception as e:
        print(f"    ECC failed: {e}")
        return None

def align_simple_resize(watermarked, original):
    """Simple resize to match dimensions"""
    print("  Using simple resize...")
    h, w = watermarked.shape[:2]
    return cv2.resize(original, (w, h))

# ============================================
# COLOR CORRECTION METHODS
# ============================================

def color_correct_histogram_matching(source, reference):
    """Match histograms channel by channel"""
    result = np.zeros_like(source)
    
    for i in range(3):
        src_hist, _ = np.histogram(source[:,:,i].flatten(), 256, [0, 256])
        ref_hist, _ = np.histogram(reference[:,:,i].flatten(), 256, [0, 256])
        
        src_cdf = src_hist.cumsum().astype(float)
        src_cdf /= src_cdf[-1]
        
        ref_cdf = ref_hist.cumsum().astype(float)
        ref_cdf /= ref_cdf[-1]
        
        lookup = np.zeros(256, dtype=np.uint8)
        ref_idx = 0
        for src_idx in range(256):
            while ref_idx < 255 and ref_cdf[ref_idx] < src_cdf[src_idx]:
                ref_idx += 1
            lookup[src_idx] = ref_idx
        
        result[:,:,i] = lookup[source[:,:,i]]
    
    return result

def color_correct_lab_transfer(source, reference):
    """Transfer color statistics in LAB color space"""
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
    reference_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB).astype(np.float32)
    
    src_mean, src_std = cv2.meanStdDev(source_lab)
    ref_mean, ref_std = cv2.meanStdDev(reference_lab)
    
    result = source_lab.copy()
    for i in range(3):
        result[:,:,i] = (result[:,:,i] - src_mean[i]) * (ref_std[i] / (src_std[i] + 1e-6)) + ref_mean[i]
    
    result = np.clip(result, 0, 255).astype(np.uint8)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

def color_correct_channel_scale(source, reference):
    """Scale each channel to match mean values"""
    result = source.astype(np.float32)
    
    for i in range(3):
        src_mean = np.mean(source[:,:,i])
        ref_mean = np.mean(reference[:,:,i])
        
        if src_mean > 0:
            result[:,:,i] = result[:,:,i] * (ref_mean / src_mean)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def color_correct_linear_regression(source, reference):
    """Use linear regression per channel for color transfer"""
    result = np.zeros_like(source)
    
    for i in range(3):
        src_flat = source[:,:,i].flatten().astype(np.float32)
        ref_flat = reference[:,:,i].flatten().astype(np.float32)
        
        # Linear regression: ref = a * src + b
        src_mean = np.mean(src_flat)
        ref_mean = np.mean(ref_flat)
        
        numerator = np.sum((src_flat - src_mean) * (ref_flat - ref_mean))
        denominator = np.sum((src_flat - src_mean) ** 2)
        
        if denominator > 0:
            a = numerator / denominator
            b = ref_mean - a * src_mean
        else:
            a = 1
            b = 0
        
        result[:,:,i] = np.clip(a * source[:,:,i].astype(np.float32) + b, 0, 255).astype(np.uint8)
    
    return result

def color_correct_polynomial(source, reference, degree=2):
    """Polynomial color transfer"""
    result = np.zeros_like(source)
    
    for i in range(3):
        src_flat = source[:,:,i].flatten().astype(np.float32)
        ref_flat = reference[:,:,i].flatten().astype(np.float32)
        
        # Sample points for fitting (using all would be slow)
        n_samples = min(10000, len(src_flat))
        indices = np.random.choice(len(src_flat), n_samples, replace=False)
        
        src_samples = src_flat[indices]
        ref_samples = ref_flat[indices]
        
        # Fit polynomial
        coeffs = np.polyfit(src_samples, ref_samples, degree)
        poly = np.poly1d(coeffs)
        
        result[:,:,i] = np.clip(poly(source[:,:,i].astype(np.float32)), 0, 255).astype(np.uint8)
    
    return result

def color_correct_hsv_transfer(source, reference):
    """Transfer color in HSV space"""
    source_hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV).astype(np.float32)
    reference_hsv = cv2.cvtColor(reference, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    # Transfer S and V channels, keep H similar
    for i in [1, 2]:  # S and V
        src_mean, src_std = cv2.meanStdDev(source_hsv[:,:,i])
        ref_mean, ref_std = cv2.meanStdDev(reference_hsv[:,:,i])
        
        source_hsv[:,:,i] = (source_hsv[:,:,i] - src_mean) * (ref_std / (src_std + 1e-6)) + ref_mean
    
    # For Hue, apply offset
    h_src_mean = np.mean(source_hsv[:,:,0])
    h_ref_mean = np.mean(reference_hsv[:,:,0])
    source_hsv[:,:,0] = (source_hsv[:,:,0] - h_src_mean + h_ref_mean) % 180
    
    source_hsv = np.clip(source_hsv, 0, 255).astype(np.uint8)
    return cv2.cvtColor(source_hsv, cv2.COLOR_HSV2BGR)

def color_correct_gamma(source, reference):
    """Gamma correction to match brightness"""
    src_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    
    src_mean = np.mean(src_gray)
    ref_mean = np.mean(ref_gray)
    
    if src_mean > 0 and ref_mean > 0:
        # Estimate gamma: ref_mean = src_mean ^ gamma
        gamma = np.log(ref_mean / 255) / np.log(src_mean / 255 + 1e-6)
        gamma = np.clip(gamma, 0.2, 5.0)
    else:
        gamma = 1.0
    
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype(np.uint8)
    
    return cv2.LUT(source, table)

# ============================================
# QUALITY METRIC
# ============================================

def calculate_alignment_quality(img1, img2):
    """Calculate how well two images match (lower = better)"""
    diff = cv2.absdiff(img1, img2)
    return np.mean(diff)

# ============================================
# MAIN FUNCTION
# ============================================

def main(watermarked_path, original_path):
    print("=" * 70)
    print("ORIGINAL IMAGE ALIGNMENT & COLOR CORRECTION")
    print("=" * 70)
    
    output_dir = create_output_dir()
    
    # Load images
    print("\nLoading images...")
    watermarked = cv2.imread(watermarked_path)
    original = cv2.imread(original_path)
    
    print(f"  Watermarked: {watermarked.shape}")
    print(f"  Original: {original.shape}")
    
    # Save inputs
    save_result(watermarked, output_dir, "00_watermarked_input")
    save_result(original, output_dir, "00_original_input")
    
    # ==========================================
    # STEP 1: TRY ALL ALIGNMENT METHODS
    # ==========================================
    
    print("\n" + "=" * 50)
    print("STEP 1: ALIGNMENT")
    print("=" * 50)
    
    alignment_methods = [
        ("orb", align_feature_matching),
        ("sift", align_sift),
        ("ecc", align_ecc),
        ("resize", align_simple_resize),
    ]
    
    aligned_versions = {}
    
    for name, method in alignment_methods:
        print(f"\n{name.upper()}:")
        result = method(watermarked, original)
        if result is not None:
            aligned_versions[name] = result
            save_result(result, output_dir, f"01_aligned_{name}")
            quality = calculate_alignment_quality(watermarked, result)
            print(f"    Quality score: {quality:.2f} (lower = better)")
    
    # ==========================================
    # STEP 2: COLOR CORRECTION FOR EACH ALIGNMENT
    # ==========================================
    
    print("\n" + "=" * 50)
    print("STEP 2: COLOR CORRECTION")
    print("=" * 50)
    
    color_methods = [
        ("histogram", color_correct_histogram_matching),
        ("lab", color_correct_lab_transfer),
        ("scale", color_correct_channel_scale),
        ("regression", color_correct_linear_regression),
        ("polynomial", color_correct_polynomial),
        ("hsv", color_correct_hsv_transfer),
        ("gamma", color_correct_gamma),
    ]
    
    all_corrected = {}
    best_score = float('inf')
    best_name = None
    best_image = None
    
    for align_name, aligned in aligned_versions.items():
        print(f"\nColor correcting '{align_name}' alignment:")
        
        for color_name, color_method in color_methods:
            try:
                corrected = color_method(aligned, watermarked)
                full_name = f"{align_name}_{color_name}"
                all_corrected[full_name] = corrected
                
                save_result(corrected, output_dir, f"02_corrected_{full_name}")
                
                quality = calculate_alignment_quality(watermarked, corrected)
                print(f"    {color_name}: {quality:.2f}")
                
                if quality < best_score:
                    best_score = quality
                    best_name = full_name
                    best_image = corrected
                    
            except Exception as e:
                print(f"    {color_name}: FAILED - {e}")
    
    # ==========================================
    # STEP 3: SAVE THE BEST RESULT
    # ==========================================
    
    print("\n" + "=" * 50)
    print("STEP 3: BEST RESULT")
    print("=" * 50)
    
    if best_image is not None:
        print(f"\n★ BEST MATCH: {best_name}")
        print(f"  Quality score: {best_score:.2f}")
        
        save_result(best_image, output_dir, "BEST_corrected_original")
        
        # Generate the difference image
        diff = cv2.absdiff(watermarked, best_image)
        save_result(diff, output_dir, "BEST_difference")
        
        # Grayscale difference
        wm_gray = cv2.cvtColor(watermarked, cv2.COLOR_BGR2GRAY)
        best_gray = cv2.cvtColor(best_image, cv2.COLOR_BGR2GRAY)
        diff_gray = cv2.absdiff(wm_gray, best_gray)
        save_result(diff_gray, output_dir, "BEST_difference_gray")
        
        # Amplified differences
        for amp in [5, 10, 20, 50, 100]:
            save_result(cv2.multiply(diff_gray, amp), output_dir, f"BEST_difference_amp{amp}")
        
        # CLAHE enhanced
        clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(diff_gray)
        save_result(enhanced, output_dir, "BEST_difference_clahe")
        
        # Thresholded
        for thresh in [3, 5, 10, 15]:
            _, binary = cv2.threshold(diff_gray, thresh, 255, cv2.THRESH_BINARY)
            save_result(binary, output_dir, f"BEST_difference_thresh{thresh}")
        
        # Inverted versions
        save_result(255 - diff_gray, output_dir, "BEST_difference_gray_inv")
        save_result(255 - cv2.multiply(diff_gray, 20), output_dir, "BEST_difference_amp20_inv")
    
    # ==========================================
    # SUMMARY
    # ==========================================
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {output_dir}/")
    print(f"\nKey files:")
    print(f"  ★ BEST_corrected_original.png  - Use this as your 'clean' original")
    print(f"  ★ BEST_difference_gray.png     - The extracted watermark")
    print(f"  ★ BEST_difference_amp20.png    - Amplified watermark (easier to see)")
    print(f"\nTo manually compare, look at the 02_corrected_*.png files")
    print(f"and pick the one that looks most like the watermarked image.")
    print("=" * 70)
    
    # Return paths for easy access
    return {
        "best_corrected": os.path.join(output_dir, "BEST_corrected_original.png"),
        "best_diff": os.path.join(output_dir, "BEST_difference_gray.png"),
        "output_dir": output_dir
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python align_and_correct.py <watermarked_image> <original_image>")
        print("Example: python align_and_correct.py watermarked.jpg original.jpg")
        sys.exit(1)
    
    watermarked_path = sys.argv[1]
    original_path = sys.argv[2]
    
    if not os.path.exists(watermarked_path):
        print(f"Error: File not found: {watermarked_path}")
        sys.exit(1)
    
    if not os.path.exists(original_path):
        print(f"Error: File not found: {original_path}")
        sys.exit(1)
    
    main(watermarked_path, original_path)