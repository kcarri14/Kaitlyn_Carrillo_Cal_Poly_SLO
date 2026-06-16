import processing.core.PImage;

import java.util.List;

public class bananaSplit extends Entity{
    public static final String BANANA_SPLIT_KEY = "banana split";
    public static final int BANANA_SPLIT_PARSE_PROPERTY_COUNT = 0;
    public bananaSplit(String id, Point position, List<PImage> images) {
        super(id, position, images);
    }
}
