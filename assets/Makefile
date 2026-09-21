TOOLS_DIR       := tools
ASSETS_DIR      := assets

HDI_DUMP_DIR    := $(ASSETS_DIR)
ARCHIVE_DIR     := $(ASSETS_DIR)/archive

PROCESSED_DIR   := $(ASSETS_DIR)/processed
SPRITES_DIR     := $(PROCESSED_DIR)/sprites
BACKGROUND_DIR  := $(PROCESSED_DIR)/backgrounds

NITROFS_DIR     := nitrofs

PACKFILE        := $(HDI_DUMP_DIR)/東方靈異.伝

PYTHON          := python3

EXTRACT_STAMP   := $(ARCHIVE_DIR)/.stamp

assets: $(EXTRACT_STAMP) $(SPRITES_DIR)/Miko.h $(SPRITES_DIR)/Miko32.h $(SPRITES_DIR)/Miko48.h $(SPRITES_DIR)/Shot.h $(SPRITES_DIR)/Orb.h $(BACKGROUND_DIR)/st0.h

$(EXTRACT_STAMP): $(PACKFILE) $(TOOLS_DIR)/extract_pf.py
	@echo "  ASSETS  extracting $(PACKFILE)"
	@mkdir -p $(ARCHIVE_DIR)
	$(PYTHON) $(TOOLS_DIR)/extract_pf.py "$(PACKFILE)" $(ARCHIVE_DIR)
	@touch $@

$(SPRITES_DIR)/Miko.h: $(EXTRACT_STAMP) $(ARCHIVE_DIR)/MIKO.PTN $(TOOLS_DIR)/ptn_to_h.py
	@echo "  ASSETS  creating Miko.h"
	$(PYTHON) $(TOOLS_DIR)/ptn_to_h.py $(ARCHIVE_DIR)/MIKO.PTN $(SPRITES_DIR) "Miko" --halve dither
	@touch $@

$(SPRITES_DIR)/Miko32.h: $(EXTRACT_STAMP) $(ARCHIVE_DIR)/MIKO_AC2.BOS $(TOOLS_DIR)/bos_to_h.py
	@echo "  ASSETS  creating Miko32.h"
	$(PYTHON) $(TOOLS_DIR)/bos_to_h.py $(ARCHIVE_DIR)/MIKO_AC2.BOS $(SPRITES_DIR) "Miko32" --halve dither
	@touch $@

$(SPRITES_DIR)/Miko48.h: $(EXTRACT_STAMP) $(ARCHIVE_DIR)/MIKO_AC.BOS $(TOOLS_DIR)/bos_to_h.py
	@echo "  ASSETS  creating Miko48.h"
	$(PYTHON) $(TOOLS_DIR)/bos_to_h.py $(ARCHIVE_DIR)/MIKO_AC.BOS $(SPRITES_DIR) "Miko48" --halve dither
	@touch $@

$(SPRITES_DIR)/Shot.h: $(EXTRACT_STAMP) $(ARCHIVE_DIR)/STG.PTN $(TOOLS_DIR)/ptn_to_h.py
	@echo "  ASSETS  creating Shot.h"
	$(PYTHON) $(TOOLS_DIR)/ptn_to_h.py $(ARCHIVE_DIR)/STG.PTN $(SPRITES_DIR) "Shot" --halve topleft -s 1 -q
	@touch $@

$(SPRITES_DIR)/Orb.h: $(EXTRACT_STAMP) $(ARCHIVE_DIR)/STG.PTN $(TOOLS_DIR)/ptn_to_h.py
	@echo "  ASSETS  creating Orb.h"
	$(PYTHON) $(TOOLS_DIR)/ptn_to_h.py $(ARCHIVE_DIR)/STG.PTN $(SPRITES_DIR) "Orb" --halve topleft -s 3 4 5 6
	@touch $@

$(BACKGROUND_DIR)/st0.h: $(EXTRACT_STAMP) $(HDI_DUMP_DIR)/ST0.GRP $(TOOLS_DIR)/grp_to_bin.py
	@echo "  ASSETS  creating st0.h and st0.bin"
	$(PYTHON) $(TOOLS_DIR)/grp_to_bin.py $(HDI_DUMP_DIR)/ST0.GRP $(BACKGROUND_DIR) $(NITROFS_DIR) "st0" --halve topleft2
	@touch $@