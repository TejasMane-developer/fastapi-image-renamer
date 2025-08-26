import zipfile
import os
import shutil
from collections import defaultdict
import re
import glob


class ZipService:
    def __init__(self):
        # Supported shapes per SKU from Excel Sheet2, including your SKU
        self.sku_supported = {
            'AFDRE11800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE12000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'pear'],
            'AFDRE12200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE12400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE12600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE12800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE13000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE13200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE13400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE13600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE13800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE14000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE14200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE14400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE14600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE14800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE15000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE15200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE15400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE15600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE15800': ['round', 'asscher', 'cushion', 'princess', 'radiant'],
            'AFDRE16000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE16200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE16400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE16600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE16800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE17000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE17200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE17400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE17600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE17800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE200': ['round', 'asscher', 'cushion', 'princess', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE1000': ['round', 'asscher', 'cushion', 'princess', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE1200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE1400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE1600': ['round', 'oval'],
            'AFDRE1800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE2000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE2200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE2400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE2600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE2800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'pear'],
            'AFDRE3000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE3200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE3400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE3600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE3800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE4000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE4200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'pear'],
            'AFDRE4400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE4600': ['round', 'oval'],
            'AFDRE4800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE5000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE5200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'pear'],
            'AFDRE5400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE5600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE5800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE6000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE6200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE6400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE6600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE6800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE7000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE7200': ['round', 'oval'],
            'AFDRE7400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE7600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE7800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE8000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE8200': ['round', 'cushion', 'princess', 'emerald', 'oval', 'marquise', 'pear'],
            'AFDRE8400': ['round', 'asscher', 'cushion', 'princess', 'oval', 'radiant'],
            'AFDRE8600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE8800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE9000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE9200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE9400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE9600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE9800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE10000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE10200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise'],
            'AFDRE10400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE10600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE10800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE11000': ['round', 'heart', 'pear'],
            'AFDRE11200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE11400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE11600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'pear'],
            'AFDRE18000': [],  # No '1's specified, so empty
            'AFDRE18200': [],  # No '1's specified, so empty
            'AFDRE18400': [],  # No '1's specified, so empty
            'AFDRE18800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE19000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE19200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE19400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE19600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE19800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE20000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE20200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE20400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE20600': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE20800': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE21000': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE21200': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear'],
            'AFDRE21400': ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear']
        }
        # Default supported shapes for unknown SKUs
        self.default_shapes = ['round', 'asscher', 'cushion', 'princess', 'emerald', 'oval', 'radiant', 'marquise', 'heart', 'pear']
        # Color mapping (for reference, not used in naming yet)
        self.color_map = {
            'yellow-gold': 'Y',
            'white-gold': 'W',
            'rose-gold': 'R',
            'yellow': 'Y',
            'white': 'W',
            'rose': 'R'
        }

    def validate_rename_inputs(self, filenames, rename_map):
        errors = []

        if not filenames:
            errors.append("Zip file is empty.")
            return errors

        if not isinstance(rename_map, dict) or not rename_map:
            errors.append("Rename map cannot be empty or invalid.")
            return errors

        shape_in_images = set()
        used_shapes_per_sku = defaultdict(set)
        unmatched_files = []

        for file_name in filenames:
            name_lower = os.path.splitext(file_name)[0].lower()
            parts = name_lower.split('_')
            if not parts:
                unmatched_files.append(file_name)
                continue

            sku = parts[0].upper()
            shape_match = re.search(r'-([a-z]+)-diamond-', name_lower)
            if shape_match:
                extracted_shape_lower = shape_match.group(1)
                matched_key = None
                for key in rename_map:
                    if key.lower() == extracted_shape_lower:
                        matched_key = key
                        break

                if matched_key:
                    shape_in_images.add(matched_key.lower())
                    used_shapes_per_sku[sku].add(matched_key.lower())
                else:
                    unmatched_files.append(file_name)
            else:
                unmatched_files.append(file_name)

        if unmatched_files:
            errors.append(f"No matching shape in rename_map for files: {', '.join(unmatched_files)}")

        # Check unused shapes in rename_map
        shape_in_rename_map = {k.lower() for k in rename_map.keys()}
        unused_shapes = shape_in_rename_map - shape_in_images
        for s in unused_shapes:
            errors.append(f"Shape '{s}' in rename_map not found in any image.")

        # Check supported shapes per SKU
        for sku, shapes in used_shapes_per_sku.items():
            supported = self.sku_supported.get(sku, self.default_shapes)
            supported = [s.lower() for s in supported]
            for shape in shapes:
                if shape not in supported:
                    errors.append(f"Shape '{shape}' not supported for SKU '{sku}' according to the configuration.")

        return errors

    def process_zip(self, zip_path, uid, rename_map: dict):
        extract_path = f"temp/{uid}/extracted"
        renamed_path = f"temp/{uid}/renamed"
        preview_dir = f"static/preview/{uid}"

        os.makedirs(extract_path, exist_ok=True)
        os.makedirs(renamed_path, exist_ok=True)
        os.makedirs(preview_dir, exist_ok=True)

        renamed_files = []
        group_counters = defaultdict(lambda: defaultdict(int))

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        filenames = sorted(os.listdir(extract_path))

        # Run validation
        validation_errors = self.validate_rename_inputs(filenames, rename_map)
        if validation_errors:
            return None, [], validation_errors

        # Continue renaming if valid
        for file_name in filenames:
            old_path = os.path.join(extract_path, file_name)
            if not os.path.isfile(old_path):
                continue

            name_without_ext, ext = os.path.splitext(file_name)
            parts = name_without_ext.split('_')
            if not parts:
                continue
            sku = parts[0]

            name_lower = name_without_ext.lower()
            shape_match = re.search(r'-([a-z]+)-diamond-', name_lower)
            if not shape_match:
                continue

            extracted_shape_lower = shape_match.group(1)
            matched_key = None
            for key in rename_map:
                if key.lower() == extracted_shape_lower:
                    matched_key = key
                    break

            if matched_key:
                group = rename_map[matched_key]
                prefix = group[0]
                try:
                    start = int(group[1:])
                except ValueError:
                    start = 1

                group_counters[sku][group] += 1
                index = start + group_counters[sku][group] - 1
                suffix = f"{prefix}{index:02d}"

                if matched_key.lower() == 'round':
                    new_name = f"{sku}_{suffix}{ext}"
                else:
                    new_name = f"{sku}_{suffix}_{matched_key.upper()}{ext}"

                new_path = os.path.join(renamed_path, new_name)

                shutil.copy(old_path, new_path)
                shutil.copy(new_path, os.path.join(preview_dir, new_name))

                renamed_files.append({
                    "old": file_name,
                    "new": new_name,
                    "url": f"/static/preview/{uid}/{new_name}"
                })

        output_zip = f"results/renamed_{uid}.zip"
        with zipfile.ZipFile(output_zip, 'w') as zf:
            for f in os.listdir(renamed_path):
                zf.write(os.path.join(renamed_path, f), f)

        shutil.rmtree(f"temp/{uid}", ignore_errors=True)

        return output_zip, renamed_files, []
    
    def cleanup(self):
        """
        Deletes all temp, preview, and results files to free disk space.
        """
        cleanup_dirs = ["temp", "static/preview", "results", "uploads"]
        removed = []

        for directory in cleanup_dirs:
            if os.path.exists(directory):
                for path in glob.glob(os.path.join(directory, "*")):
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                        removed.append(path)
                    except Exception as e:
                        removed.append(f"Failed: {path} ({e})")

        return removed
